# -*- coding: utf-8 -*-
"""
#/*
##; Copyright (c) 2010-2021, Armin Ronacher(BSD-3-Clause)
##; All rights reserved.
##; 
##; @@@Origin: https://github.com/pallets-eco/flask-sqlalchemy/blob/2.5.1/flask_sqlalchemy/__init__.py
##; 
##; This module is part of SQLAlchemy and is released under
##; the BSD-3-Clause License: https://opensource.org/license/bsd-3-clause
##; details as below:
#*
#* Redistribution and use in source and binary forms, with or without
#* modification, are permitted provided that the following conditions are met:
#*
#* 1. Redistributions of source code must retain the above copyright notice, this
#*    list of conditions and the following disclaimer.
#*
#* 2. Redistributions in binary form must reproduce the above copyright notice,
#*    this list of conditions and the following disclaimer in the documentation
#*    and/or other materials provided with the distribution.
#*
#* 3. Neither the name of the copyright holder nor the names of its
#*    contributors may be used to endorse or promote products derived from
#*    this software without specific prior written permission.
#*
#* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#* FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#* DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#* SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#*/
"""

from __future__ import absolute_import

import os
import warnings
from threading import Lock

import sqlalchemy
import flask
from sqlalchemy import orm
from sqlalchemy.engine.url import make_url
from sqlalchemy.engine import Connection
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.orm.session import Session as SessionBase

from .model import DefaultMeta, DeclarativeMeta, declarative_base
from .model import Model
from ._compat import itervalues, string_types, _ident_func
from ._adapt import FsaAppAdaptor, FsaAdaptError
from . import utils
from . import _sa_help as sa_help


class SignallingSession(SessionBase):
    """The signalling session is the default session that Flask-SQLAlchemy
    uses.  It extends the default session system with bind selection and
    modification tracking.

    If you want to use a different session you can override the
    :meth:`SQLAlchemy.create_session` function.

    .. versionadded:: 2.0

    .. versionadded:: 2.1
        The `binds` option was added, which allows a session to be joined
        to an external transaction.
    """

    def __init__(
        self,
        fsa: FsaAppAdaptor, autocommit=False,
        autoflush=True,
        bind=None,
        binds=None,
        **options
    ):
        #: The application that this session belongs to.
        self._fsa = fsa  # type: (FsaAppAdaptor, SQLAlchemy)
        self._app = fsa.get_app(nullable=True)
        # track_modifications = app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
        if isinstance(fsa, SQLAlchemy):
            if bind is None:
                bind = fsa.engine
            if binds is None:
                binds = fsa.get_binds(self._app)

        if fsa.cfg_option("SQLALCHEMY_TRACK_MODIFICATIONS", False):
            sa_help._SessionSignalEvents.register(self)

        SessionBase.__init__(
            self, autocommit=autocommit, autoflush=autoflush,
            bind=bind, binds=binds, **options
        )

    @property
    def app(self):
        if self._app is None:
            self._app = self._fsa.get_app(self._app)
        return self._app

    def get_bind(self, mapper=None, clause=None):
        """Return the engine or connection for a given model or
        table, using the ``__bind_key__`` if it is set.
        """
        # mapper is None if someone tries to just get a connection
        if mapper is not None:
            try:
                # SA >= 1.3
                persist_selectable = mapper.persist_selectable
            except AttributeError:
                # SA < 1.3
                persist_selectable = mapper.mapped_table

            info = getattr(persist_selectable, 'info', {})
            bind_key = info.get('bind_key')
            if bind_key is not None and isinstance(self._fsa, SQLAlchemy):
                return self._fsa.get_engine(bind=bind_key)
        return SessionBase.get_bind(self, mapper, clause)  # type: Connection 


class _QueryProperty(object):
    def __init__(self, fsa):
        self.sa = fsa
        self._fsa = fsa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            if mapper:
                return type.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:
            return None


class _EngineConnector(FsaAppAdaptor):
    def __init__(self, fsa: FsaAppAdaptor, app=None, bind=None, **kwargs):
        self._fsa = fsa  # type: (FsaAppAdaptor, SQLAlchemy)
        self._app = app
        self._bind_key = bind
        self._ori_db_uri = self.get_uri(nullable=True)
        self._ori_db_echo = False
        ###; lazy loads, dynamic modify
        self._engine = None
        self._connected_for = None
        self._lock = Lock()
        self._engine_options = kwargs.get("engine_options", {})
        if self.check_debug():
            self.get_engine = self._check_engine
        else:
            self.get_engine = self._fetch_engine

    @property
    def app_config(self):
        return self._fsa.app_config

    def get_app(self, nullable=True, **kwargs):
        return self._fsa.get_app(nullable=nullable, **kwargs)

    def __repr__(self):
        return f"<_EngineConnector:{self._fsa}>"

    def get_uri(self, nullable=False, **kwargs):
        if self._bind_key is None:
            return self.cfg_option('SQLALCHEMY_DATABASE_URI', nullable=nullable, **kwargs)
        binds = self.cfg_option('SQLALCHEMY_BINDS', default_value={}, nullable=True)  # type: dict
        uri = ""
        if isinstance(binds, dict):
            uri = binds.get(self._bind_key, "")

        if not uri:
            msg = 'Bind %r is not specified.  Set it in the SQLALCHEMY_BINDS ' \
                  'configuration variable' % self._bind_key
            if not nullable:
                raise FsaAdaptError(msg, binds=binds, bind_key=self._bind_key)
            else:
                warnings.warn(msg)
        return uri  # type:str

    def _fetch_engine(self):
        ##; better performance, Origin Flask-Sqlalchemy
        with self._lock:
            if self._engine is None:
                if not self._ori_db_uri:
                    self._ori_db_uri = self.get_uri(nullable=False)

                sa_url = make_url(self._ori_db_uri)
                options = self.get_engine_options(sa_url, self._ori_db_echo)
                self._engine = sqlalchemy.create_engine(sa_url, **options)
                self._connected_for = (self._ori_db_uri, self._ori_db_echo)
            return self._engine  # type: sqlalchemy.engine.Engine

    def _check_engine(self):
        ##; lower performance, Origin Flask-Sqlalchemy
        with self._lock:
            uri = self.get_uri(nullable=False)
            echo = self.cfg_option('SQLALCHEMY_ECHO', default_value=bool(self.check_debug()))
            if (uri, echo) == self._connected_for:
                return self._engine

            sa_url = make_url(uri)
            options = self.get_engine_options(sa_url, echo)
            self._engine = rv = sqlalchemy.create_engine(sa_url, **options)

            if self._app is not None:
                if self.check_debug():
                    app_imp_name = getattr(
                        self._app, "import_name",
                        self.cfg_option("APP_IMPORT_NAME", default_value=str(self._app))
                    )
                    sa_help._EngineDebuggingSignalEvents(
                        self._engine,
                        app_imp_name,
                    ).register()

            self._connected_for = (uri, echo)

            return rv  # type: sqlalchemy.engine.Engine

    def get_engine_options(self, sa_url, echo=False):
        if self._engine_options:
            return self._engine_options

        options = {}
        options = self.apply_pool_defaults(self._app, options)
        sa_url, options = self.apply_driver_hacks(self._app, sa_url, options)

        if echo:
            options['echo'] = echo

        ##; Give the config options set by a developer explicitly priority
        ##; over decisions FSA makes.
        opts = self.cfg_option('SQLALCHEMY_ENGINE_OPTIONS', default_value={})
        options.update(opts)

        ##; Give options set in SQLAlchemy.__init__() ultimate priority
        opt2 = getattr(self._fsa, "_engine_options", {})
        if opt2 and isinstance(opt2, dict):
            options.update(opt2)

        self._engine_options = options
        return options


class _SQLAlchemyState(object):
    """Remembers configuration for the (db, app) tuple."""

    def __init__(self, db):
        self.db = db  # type: SQLAlchemy
        self.connectors = {}


class SQLAlchemy(FsaAppAdaptor):
    """This class is used to control the SQLAlchemy integration to one
    or more Flask applications.  Depending on how you initialize the
    object it is usable right away or will attach as needed to a
    Flask application.

    There are two usage modes which work very similarly.  One is binding
    the instance to a very specific Flask application::

        app = Flask(__name__)
        db = SQLAlchemy(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        db = SQLAlchemy()

        def create_app():
            app = Flask(__name__)
            db.init_app(app)
            return app

    The difference between the two is that in the first case methods like
    :meth:`create_all` and :meth:`drop_all` will work all the time but in
    the second case a :meth:`flask.Flask.app_context` has to exist.

    By default Flask-SQLAlchemy will apply some backend-specific settings
    to improve your experience with them.

    As of SQLAlchemy 0.6 SQLAlchemy
    will probe the library for native unicode support.  If it detects
    unicode it will let the library handle that, otherwise do that itself.
    Sometimes this detection can fail in which case you might want to set
    ``use_native_unicode`` (or the ``SQLALCHEMY_NATIVE_UNICODE`` configuration
    key) to ``False``.  Note that the configuration key overrides the
    value you pass to the constructor.  Direct support for ``use_native_unicode``
    and SQLALCHEMY_NATIVE_UNICODE are deprecated as of v2.4 and will be removed
    in v3.0.  ``engine_options`` and ``SQLALCHEMY_ENGINE_OPTIONS`` may be used
    instead.

    This class also provides access to all the SQLAlchemy functions and classes
    from the :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` modules.  So you can
    declare models like this::

        class User(db.Model):
            username = db.Column(db.String(80), unique=True)
            pw_hash = db.Column(db.String(80))

    You can still use :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` directly, but
    note that Flask-SQLAlchemy customizations are available only through an
    instance of this :class:`SQLAlchemy` class.  Query classes default to
    :class:`BaseQuery` for `db.Query`, `db.Model.query_class`, and the default
    query_class for `db.relationship` and `db.backref`.  If you use these
    interfaces through :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` directly,
    the default query class will be that of :mod:`sqlalchemy`.

    .. admonition:: Check types carefully

       Don't perform type or `isinstance` checks against `db.Table`, which
       emulates `Table` behavior but is not a class. `db.Table` exposes the
       `Table` interface, but is a function which allows omission of metadata.

    The ``session_options`` parameter, if provided, is a dict of parameters
    to be passed to the session constructor.  See :class:`~sqlalchemy.orm.session.Session`
    for the standard options.

    The ``engine_options`` parameter, if provided, is a dict of parameters
    to be passed to create engine.  See :func:`~sqlalchemy.create_engine`
    for the standard options.  The values given here will be merged with and
    override anything set in the ``'SQLALCHEMY_ENGINE_OPTIONS'`` config
    variable or othewise set by this library.

    .. versionadded:: 0.10
       The `session_options` parameter was added.

    .. versionadded:: 0.16
       `scopefunc` is now accepted on `session_options`. It allows specifying
        a custom function which will define the SQLAlchemy session's scoping.

    .. versionadded:: 2.1
       The `metadata` parameter was added. This allows for setting custom
       naming conventions among other, non-trivial things.

       The `query_class` parameter was added, to allow customisation
       of the query class, in place of the default of :class:`BaseQuery`.

       The `model_class` parameter was added, which allows a custom model
       class to be used in place of :class:`Model`.

    .. versionchanged:: 2.1
       Utilise the same query class across `session`, `Model.query` and `Query`.

    .. versionadded:: 2.4
       The `engine_options` parameter was added.

    .. versionchanged:: 2.4
       The `use_native_unicode` parameter was deprecated.

    .. versionchanged:: 2.4.3
        ``COMMIT_ON_TEARDOWN`` is deprecated and will be removed in
        version 3.1. Call ``db.session.commit()`` directly instead.

    ========================================================
    ##; flask-sqlalchemy==2.5.1 >>> PysqlOrm==2.5.3 
    ========================================================    
    .. versionchanged:: 2.5.3
        query_class change defaults from class:`BaseQuery(FsaQuery)` to `orm.Query`
        lazyload with default as None 
        
    """

    #: Default query class used by :attr:`Model.query` and other queries.
    #: Customize this by passing ``query_class`` to :func:`SQLAlchemy`.
    Query = None

    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=None, model_class=Model,
                 _app_framework="flask", **kwargs
                 ):
        ##; dirty for Decoupling failed on Query-Model-session 
        if query_class is None:
            if app is None:
                query_class = orm.Query
                _app_framework = ""
            elif _app_framework == "flask":
                from .exts._flask import FsaQuery
                query_class = FsaQuery
            else:
                ##; Defaults to :class:`orm.Query` 
                query_class = orm.Query

        self._app_config = kwargs.get("app_config", {})
        self._conn_state = None
        self._app = app

        self._app_framework = _app_framework
        self._model_class = model_class
        self._engine_options = kwargs.get("engine_options", {})
        self._engine_lock = Lock()

        self.use_native_unicode = use_native_unicode
        self.Query = query_class
        self.Model = self.make_declarative_base(model_class, metadata)
        self.session = self.create_scoped_session(session_options)

        sa_help._include_sqlalchemy(self, query_class)
        if app is not None:
            self.init_app(app, app_framework=_app_framework)
        self.init_config()

    @property
    def metadata(self):
        """The metadata associated with ``db.Model``."""

        return self.Model.metadata

    def create_scoped_session(self, options=None):
        """Create a :class:`~sqlalchemy.orm.scoping.scoped_session`
        on the factory from :meth:`create_session`.

        An extra key ``'scopefunc'`` can be set on the ``options`` dict to
        specify a custom scope function.  If it's not provided, Flask's app
        context stack identity is used. This will ensure that sessions are
        created and removed with the request/response cycle, and should be fine
        in most cases.

        :param options: dict of keyword arguments passed to session class  in
            ``create_session``
        """

        if options is None:
            options = {}

        scopefunc = options.pop('scopefunc', _ident_func)
        options.setdefault('query_cls', self.Query)
        return orm.scoped_session(
            self.create_session(options), scopefunc=scopefunc
        )

    def create_session(self, options):
        """Create the session factory used by :meth:`create_scoped_session`.

        The factory **must** return an object that SQLAlchemy recognizes as a session,
        or registering session events may raise an exception.

        Valid factories include a :class:`~sqlalchemy.orm.session.Session`
        class or a :class:`~sqlalchemy.orm.session.sessionmaker`.

        The default implementation creates a ``sessionmaker`` for :class:`SignallingSession`.

        :param options: dict of keyword arguments passed to session class
        """
        # bind = options.pop('bind', None) or self.engine
        # binds = options.pop('binds', self.get_binds(self._app))
        return orm.sessionmaker(
            class_=SignallingSession, fsa=self,
            # bind=bind, binds=binds,
            **options
        )

    def make_declarative_base(self, model, metadata=None):
        """Creates the declarative base that all models will inherit from.

        :param model: base model class (or a tuple of base classes) to pass
            to :func:`~sqlalchemy.ext.declarative.declarative_base`. Or a class
            returned from ``declarative_base``, in which case a new base class
            is not created.
        :param metadata: :class:`~sqlalchemy.MetaData` instance to use, or
            none to use SQLAlchemy's default.

        .. versionchanged 2.3.0::
            ``model`` can be an existing declarative base in order to support
            complex customization such as changing the metaclass.
        """
        if not isinstance(model, DeclarativeMeta):
            model = declarative_base(
                cls=model,
                name='Model',
                metadata=metadata,
                metaclass=DefaultMeta
            )

        # if user passed in a declarative base and a metaclass for some reason,
        # make sure the base uses the metaclass
        if metadata is not None and model.metadata is not metadata:
            model.metadata = metadata

        if not getattr(model, 'query_class', None):
            model.query_class = self.Query

        model.query = _QueryProperty(self)
        return model


    def init_config(self):
        cfg = self.make_config(self.app_config)
        ##; Deprecation warnings for config keys that should be replaced by SQLALCHEMY_ENGINE_OPTIONS.
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_POOL_SIZE', 'pool_size')
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_POOL_TIMEOUT', 'pool_timeout')
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_POOL_RECYCLE', 'pool_recycle')
        utils.engine_config_warning(cfg, '3.0', 'SQLALCHEMY_MAX_OVERFLOW', 'max_overflow')
        return cfg


    def __init_app(self, app, cfg=None):
        """This callback can be used to initialize an application for the
        use with this database setup.  Never use a database in the context
        of an application not initialized that way or connections will
        leak.
        """
        if cfg is None:
            cfg = getattr(app, "config", None)
            if isinstance(cfg, dict):
                if not self.app_config:
                    self.app_config = cfg
                else:
                    self.update_config(**cfg)
            else:
                warnings.warn(f'[{self}]: app.config is not set!')

        if (
            'SQLALCHEMY_DATABASE_URI' not in cfg and
            'SQLALCHEMY_BINDS' not in cfg
        ):
            warnings.warn(
                'Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set. '
                'Defaulting SQLALCHEMY_DATABASE_URI to "sqlite:///:memory:".'
            )

        ## app.extensions['sqlalchemy'] = _SQLAlchemyState(self)
        exts = getattr(app, "extensions", {})
        exts['sqlalchemy'] = self.get_state(app)
        app.extensions = exts

    def init_app(self, app, cfg=None, app_framework="flask"):
        ##; TODO@NICO: app_framework use enum-strings
        if app_framework == "flask" or isinstance(app, flask.Flask):
            self._app_framework = "flask"
            self.init_flask_app(app, cfg)
        elif app is not None:
            warnings.warn(f"Unknown APP({app}): {type(app)} ???")
            self.__init_app(app, cfg)
        else:
            raise RuntimeError(f"{self}: Invalid init_app(None)")

    def init_flask_app(self, app, cfg=None):
        self.__init_app(app, cfg=cfg)

        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            if self.cfg_option('SQLALCHEMY_COMMIT_ON_TEARDOWN'):
                warnings.warn(
                    "'COMMIT_ON_TEARDOWN' is deprecated and will be"
                    " removed in version 3.1. Call"
                    " 'db.session.commit()'` directly instead.",
                    DeprecationWarning,
                )

                if response_or_exc is None:
                    self.session.commit()

            self.session.remove()
            return response_or_exc

    @property
    def engine(self):
        """Gives access to the engine.  If the database configuration is bound
        to a specific application (initialized with an application) this will
        always return a database connection.  If however the current application
        is used this might raise a :exc:`RuntimeError` if no application is
        active at the moment.
        """
        return self.get_engine()

    @property
    def engine_options(self):
        if self._engine_options:
            return self._engine_options
        else:
            opt = self.cfg_option("SQLALCHEMY_ENGINE_OPTIONS", default_value={})
            return opt

    def make_connector(self, app=None, bind=None):
        """Creates the connector for a given state and bind."""
        app_ = self.get_app(app, nullable=True)
        return _EngineConnector(self, app=app_, bind=bind, engine_options=self.engine_options)


    def get_state(self, app=None):
        fsa = self._conn_state
        app2 = self.get_app(app, nullable=True)
        if app2 is None:
            if fsa is None:
                fsa = _SQLAlchemyState(self)
                self._conn_state = fsa
            return fsa
        else:
            ext = getattr(app2, "extensions", {})
            sa = ext.get("sqlalchemy", fsa)
            if sa is None:
                if fsa is None:
                    sa = _SQLAlchemyState(self)
                    self._conn_state = sa
                else:
                    sa = fsa

            ext.update(sqlalchemy=sa)
            setattr(app2, "extensions", ext)
            return sa


    def get_engine(self, app=None, bind=None):
        """
            Returns a specific engine.
            `_EngineConnector(self).get_engine()`
        """

        state = self.get_state(app)  # type: _SQLAlchemyState

        with self._engine_lock:
            connector = state.connectors.get(bind)

            if connector is None:
                connector = self.make_connector(app, bind)  # type: _EngineConnector
                state.connectors[bind] = connector

            return connector.get_engine()  # type: sqlalchemy.engine.Engine 


    def create_engine(self, sa_url, engine_opts):
        """
            Override this method to have final say over how the SQLAlchemy engine
            is created.

            In most cases, you will want to use ``'SQLALCHEMY_ENGINE_OPTIONS'``
            config variable or set ``engine_options`` for :func:`SQLAlchemy`.
        """
        return sqlalchemy.create_engine(sa_url, **engine_opts)


    def get_app(self, reference_app=None, nullable=False):
        """Helper method that implements the logic to look up an
        application."""

        if reference_app is not None:
            return reference_app

        if flask.has_app_context():
            return flask.current_app  # type: flask.Flask

        if self._app is not None:
            return self._app

        if nullable:
            return None

        raise RuntimeError(
            'No application found. Either work inside a view function or push'
            ' an application context. See'
            ' http://flask-sqlalchemy.pocoo.org/contexts/.'
        )

    def get_tables_for_bind(self, bind=None):
        """Returns a list of all tables relevant for a bind."""
        result = []
        for table in itervalues(self.Model.metadata.tables):
            if table.info.get('bind_key') == bind:
                result.append(table)
        return result

    def get_binds(self, app=None):
        """Returns a dictionary with a table->engine mapping.

        This is suitable for use of sessionmaker(binds=db.get_binds(app)).
        """
        app = self.get_app(app, nullable=True)
        binds = [None] + list(self.cfg_option('SQLALCHEMY_BINDS', default_value=()))
        retval = {}
        for bind in binds:
            engine = self.get_engine(app, bind)
            tables = self.get_tables_for_bind(bind)
            retval.update(dict((table, engine) for table in tables))
        return retval

    def _execute_for_all_tables(self, app, bind, operation, skip_tables=False):
        app = self.get_app(app, nullable=True)

        if bind == '__all__':
            binds = [None] + list(self.cfg_option('SQLALCHEMY_BINDS', default_value=()))
        elif isinstance(bind, string_types) or bind is None:
            binds = [bind]
        else:
            binds = bind

        for bind in binds:
            extra = {}
            if not skip_tables:
                tables = self.get_tables_for_bind(bind)
                extra['tables'] = tables
            op = getattr(self.Model.metadata, operation)
            op(bind=self.get_engine(app, bind), **extra)

    def create_all(self, bind='__all__', app=None):
        """Creates all tables.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'create_all')

    def drop_all(self, bind='__all__', app=None):
        """Drops all tables.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'drop_all')

    def reflect(self, bind='__all__', app=None):
        """Reflects tables from the database.

        .. versionchanged:: 0.12
           Parameters were added
        """
        self._execute_for_all_tables(app, bind, 'reflect', skip_tables=True)

    def __repr__(self):
        s = super(SQLAlchemy, self).__repr__()
        return f"{s}:{self.get_uri(safety_wrap=self.check_debug())}"

    @property
    def app(self):
        return self.get_app(self._app)
