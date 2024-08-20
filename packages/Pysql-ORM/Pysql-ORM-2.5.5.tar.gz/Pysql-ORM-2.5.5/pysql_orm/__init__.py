# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sqlalchemy  # noqa
from . import utils, _adapt, _compat
from ._compat import itervalues, string_types, xrange
from ._signals import before_models_committed, signals_available, models_committed
from ._adapt import FsaAdaptError, FSADeprecationWarning, FsaAppAdaptor
from .model import DefaultMeta
from .model import Model
from .exports import SQLAlchemy


version_info = (2, 5, 5)
__version__ = "2.5.5"

##; Copyright (c) 2010-2021, Armin Ronacher(BSD-3-Clause)
_statement_of_refered_packages = {
    "flask-sqlalchemy": dict(
        version="2.5.1",
        RepoUrl="https://github.com/pallets-eco/flask-sqlalchemy/tree/2.5.1",
        License="BSD-3-Clause"
    )
}

__all__ = [
    sqlalchemy,
    SQLAlchemy,
    Model,
    DefaultMeta,
    FsaAdaptError,
    FSADeprecationWarning,
    

]