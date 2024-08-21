# -*- python -*-
# Copyright (C) 2024 Cardiff University
# SPDX-License-Identifier: Apache-2.0

"""SciToken plugin for Requests.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from .auth import HTTPSciTokenAuth
from .requests import (
    delete,
    get,
    head,
    patch,
    post,
    put,
)
from .sessions import (
    Session,
    SessionMixin,
)

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = ''
