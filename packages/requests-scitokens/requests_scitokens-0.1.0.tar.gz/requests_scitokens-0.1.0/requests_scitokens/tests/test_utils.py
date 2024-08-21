# -*- python -*-
# Copyright (C) 2024 Cardiff University
# SPDX-License-Identifier: Apache-2.0

"""Tests for :mod:`requests_scitokens.utils`
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import pytest

from requests_scitokens import utils as rsutils


@pytest.mark.parametrize(("url", "kwargs", "aud"), (
    # basic
    ("https://example.com/data", {}, "https://example.com"),
    # default scheme
    ("example.com", {}, "https://example.com"),
    # port
    ("https://example.com:443/data/test", {}, "https://example.com"),
    # non-default scheme
    ("http://example.com:443/data/test", {}, "http://example.com"),
    # keyword scheme
    ("example.com:443/data/test", {"scheme": "xroot"}, "xroot://example.com"),
))
def test_default_audience(url, kwargs, aud):
    """Test :func:`requests_scitokens.utils.default_audience`.
    """
    assert rsutils.default_audience(url, **kwargs) == aud
