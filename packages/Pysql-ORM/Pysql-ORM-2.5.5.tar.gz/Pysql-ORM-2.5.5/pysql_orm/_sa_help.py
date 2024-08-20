# -*- coding: utf-8 -*-
"""
## __version__ = "2.5.1"
##; https://github.com/pallets-eco/flask-sqlalchemy/blob/2.5.1/flask_sqlalchemy/__init__.py
"""

from __future__ import absolute_import

import functools
import sys

from operator import itemgetter

import flask
import sqlalchemy
from sqlalchemy import event, inspect, orm

from ._compat import string_types, _timer
from ._signals import before_models_committed, models_committed


def _sa_url_set(url: sqlalchemy.engine.URL, **kwargs):
    try:
        url = url.set(**kwargs)
    except AttributeError:
        # SQLAlchemy <= 1.3
        for key, value in kwargs.items():
            setattr(url, key, value)

    return url


def _sa_url_query_setdefault(url, **kwargs):
    query = dict(url.query)

    for key, value in kwargs.items():
        query.setdefault(key, value)

    return _sa_url_set(url, query=query)


def _make_table(db):
    def _make_table(*args, **kwargs):
        if len(args) > 1 and isinstance(args[1], db.Column):
            args = (args[0], db.metadata) + args[1:]
        info = kwargs.pop('info', None) or {}
        info.setdefault('bind_key', None)
        kwargs['info'] = info
        return sqlalchemy.Table(*args, **kwargs)

    return _make_table


def _set_default_query_class(d, cls):
    if 'query_class' not in d:
        d['query_class'] = cls


def _wrap_with_default_query_class(fn, cls):
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        _set_default_query_class(kwargs, cls)
        if "backref" in kwargs:
            backref = kwargs['backref']
            if isinstance(backref, string_types):
                backref = (backref, {})
            _set_default_query_class(backref[1], cls)
        return fn(*args, **kwargs)

    return newfn


def _include_sqlalchemy(obj, cls):
    for module in sqlalchemy, sqlalchemy.orm:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))
    # Note: obj.Table does not attempt to be a SQLAlchemy Table class.
    obj.Table = _make_table(obj)
    obj.relationship = _wrap_with_default_query_class(obj.relationship, cls)
    obj.relation = _wrap_with_default_query_class(obj.relation, cls)
    obj.dynamic_loader = _wrap_with_default_query_class(obj.dynamic_loader, cls)
    obj.event = event


class _DebugQueryTuple(tuple):
    statement = property(itemgetter(0))
    parameters = property(itemgetter(1))
    start_time = property(itemgetter(2))
    end_time = property(itemgetter(3))
    context = property(itemgetter(4))

    @property
    def duration(self):
        return self.end_time - self.start_time

    def __repr__(self):
        return '<query statement="%s" parameters=%r duration=%.03f>' % (
            self.statement,
            self.parameters,
            self.duration
        )


def _calling_context(app_path):
    frm = sys._getframe(1)
    while frm.f_back is not None:
        name = frm.f_globals.get('__name__')
        if name and (name == app_path or name.startswith(app_path + '.')):
            funcname = frm.f_code.co_name
            return '%s:%s (%s)' % (
                frm.f_code.co_filename,
                frm.f_lineno,
                funcname
            )
        frm = frm.f_back
    return '<unknown>'


class _SessionSignalEvents(object):
    @classmethod
    def register(cls, session):
        if not hasattr(session, '_model_changes'):
            session._model_changes = {}

        event.listen(session, 'before_flush', cls.record_ops)
        event.listen(session, 'before_commit', cls.record_ops)
        event.listen(session, 'before_commit', cls.before_commit)
        event.listen(session, 'after_commit', cls.after_commit)
        event.listen(session, 'after_rollback', cls.after_rollback)

    @classmethod
    def unregister(cls, session):
        if hasattr(session, '_model_changes'):
            del session._model_changes

        event.remove(session, 'before_flush', cls.record_ops)
        event.remove(session, 'before_commit', cls.record_ops)
        event.remove(session, 'before_commit', cls.before_commit)
        event.remove(session, 'after_commit', cls.after_commit)
        event.remove(session, 'after_rollback', cls.after_rollback)

    @staticmethod
    def record_ops(session, flush_context=None, instances=None):
        try:
            d = session._model_changes
        except AttributeError:
            return
        ss_opts = (
            (session.new, 'insert'),
            (session.dirty, 'update'),
            (session.deleted, 'delete')
        )
        for targets, operation in ss_opts:
            for target in targets:
                state = inspect(target)
                key = state.identity_key if state.has_identity else id(target)
                d[key] = (target, operation)

    @staticmethod
    def before_commit(session):
        try:
            d = session._model_changes
        except AttributeError:
            return

        if d:
            before_models_committed.send(
                session.app, changes=list(d.values())
            )

    @staticmethod
    def after_commit(session):
        try:
            d = session._model_changes
        except AttributeError:
            return

        if d:
            models_committed.send(
                session.app, changes=list(d.values())
            )
            d.clear()

    @staticmethod
    def after_rollback(session):
        try:
            d = session._model_changes
        except AttributeError:
            return

        d.clear()


class _EngineDebuggingSignalEvents(object):
    """Sets up handlers for two events that let us track the execution time of
    queries."""

    def __init__(self, engine, import_name):
        self.engine = engine
        self.app_package = import_name

    def register(self):
        event.listen(
            self.engine, 'before_cursor_execute',
            self.before_cursor_execute
        )
        event.listen(
            self.engine, 'after_cursor_execute',
            self.after_cursor_execute
        )

    def before_cursor_execute(
        self, conn, cursor, statement, parameters, context, executemany
    ):
        if flask.has_app_context():
            context._query_start_time = _timer()

    def after_cursor_execute(
        self, conn, cursor, statement, parameters, context, executemany
    ):
        if flask.has_app_context():
            # try:
            #     queries = flask._app_ctx_stack.top.sqlalchemy_queries
            # except AttributeError:
            #     queries = flask._app_ctx_stack.top.sqlalchemy_queries = []

            queries = getattr(flask._app_ctx_stack.top, "sqlalchemy_queries", [])
            flask._app_ctx_stack.top.sqlalchemy_queries = queries
            queries.append(
                _DebugQueryTuple(
                    (
                        statement, parameters, context._query_start_time,
                        _timer(), _calling_context(self.app_package),
                    )
                )
            )
