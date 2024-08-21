# -*- python -*-
# Copyright (C) 2024 Cardiff University
# SPDX-License-Identifier: Apache-2.0

"""Session API for requests-scitokens.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import requests

from requests_scitokens.auth import HTTPSciTokenAuth


class SessionMixin():
    def __init__(self, *args, auth=None, token=None, **kwargs):
        if auth is None:
            auth = HTTPSciTokenAuth(token=token)
        super().__init__(*args, auth=auth, **kwargs)


class Session(SessionMixin, requests.Session):
    pass
