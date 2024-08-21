# -*- python -*-
# Copyright (C) 2024 Cardiff University
# SPDX-License-Identifier: Apache-2.0

"""Request API for requests-scitokens.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from functools import wraps

import requests.api

from requests_scitokens.auth import HTTPSciTokenAuth
from requests_scitokens.utils import default_audience


@wraps(requests.request)
def request(method, url, *args, auth=None, session=None, **kwargs):
    """Send a SciToken-aware request.

    Parameters
    ----------
    method : `str`
        The method to use.

    url : `str`,
        The URL to request.

    session : `requests.Session`, optional
        The connection session to use, if not given one will be
        created on-the-fly.

    args, kwargs
        All other keyword arguments are passed directly to
        `requests.Session.request`

    Returns
    -------
    resp : `requests.Response`
        the response object

    See also
    --------
    igwn_auth_utils.requests.Session.request
        for information on how the request is performed
    """
    if auth is None:
        auth = HTTPSciTokenAuth(
            token=kwargs.get("token"),
            audience=kwargs.get("audience", default_audience(url)),
        )

    if not session:  # use module
        session = requests
    return session.request(method, url, *args, auth=auth, **kwargs)


def _request_wrapper_factory(method):
    """Factor function to wrap a :mod:`requests` HTTP method to use
    our request function.
    """
    @wraps(getattr(requests.api, method))
    def _request_wrapper(url, *args, session=None, **kwargs):
        return request(method, url, *args, session=session, **kwargs)

    return _request_wrapper


# request methods
delete = _request_wrapper_factory("delete")
get = _request_wrapper_factory("get")
head = _request_wrapper_factory("head")
patch = _request_wrapper_factory("patch")
post = _request_wrapper_factory("post")
put = _request_wrapper_factory("put")
