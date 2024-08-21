# -*- python -*-
# Copyright (C) 2024 Cardiff University
# SPDX-License-Identifier: Apache-2.0

"""Auth plugin for SciToken requests.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

from requests.auth import AuthBase as _AuthBase
from requests.utils import (
    parse_dict_header,
    parse_list_header,
)

from scitokens import SciToken

from requests_scitokens.utils import (
    default_audience,
    serialize_token,
)


def _www_authenticate_bearer_params(response):
    """Return the WWW-Authenticate Bearer response auth-params if found.

    See RFC 6750, section 3.

    Returns
    -------
    params : `False`, `dict`
        Either `False` if the ``www-authenticate`` header is not present,
        or doesn't challenege Bearer auth, or a `dict` (possible empty)
        of params to use in the Bearer challenge.
    """
    try:
        wwwauth = response.headers["www-authenticate"]
    except KeyError:
        return False

    for authopt in parse_list_header(wwwauth):
        # if header is just 'Bearer', then return empty dict
        if authopt == "Bearer":
            return {}
        # otherwise if header starts with Bearer and some whitespace
        # extract the params  -- this just avoids falsely matching
        # something like 'Bearer2', which we don't understand.
        if authopt.startswith("Bearer "):  # with params
            return parse_dict_header(authopt[6:])

    # no match
    return False


class HTTPSciTokenAuth(_AuthBase):
    """Auth handler for SciTokens.

    Parameters
    ----------
    token : `scitokens.SciToken`, `None`
        The `~scitokens.SciToken` to use for bearer authorisation.
        Pass `None` to dynamically discover a token for each request.

    audience : `str`
        The ``aud`` claim to require when discovering tokens.

    force : `bool`
        If `True`, preemptively discover a token and generate an
        ``Authorization`` header for all requests.

        If `False`, wait for the remote server to respond with an
        authorisation challenge via a 401 ``Unauthorized`` response
        that includes a ``WWW-Authenticate`` header.
    """
    def __init__(
        self,
        token=None,
        audience=None,
        force=False,
    ):
        self.token = token
        self.audience = audience
        self.force = force

    def __eq__(self, other):
        return all([
            self.token == getattr(other, "token", None),
            self.audience == getattr(other, "audience", None),
            self.force == getattr(other, "force", False),
        ])

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def _auth_header_str(token, auth_scheme="Bearer"):
        """Serialise a `scitokens.SciToken` and format an Authorization header.

        Parameters
        ----------
        token : `scitokens.SciToken`, `str`, `bytes`
            The token to serialize, or an already serialized representation.

        auth_scheme : `str`
            The authorisation scheme to use, defaults to ``"Bearer"``.
        """
        if not isinstance(token, (str, bytes)):
            token = serialize_token(token)
        return f"{auth_scheme} {token}"

    def find_token(
        self,
        url=None,
        error=True,
        find_func=SciToken.discover,
        **discover_kwargs,
    ):
        """Find a bearer token for authorization.

        Parameters
        ----------
        url : `str`
            The URL that will be queried.

        error : `bool`
            If `True`, `raise` exceptions, otherwise return `None`.

        find_func : `callable`
            The function to call to discover SciTokens, defaults
            to :meth:`~scitokens.SciToken.discover`.

        discover_kwargs
            Other keyword arguments to pass to ``find_func``.

        Returns
        -------
        token : `scitokens.SciToken`, `None`
            The discovered token, or `None` if a token is not foudn
            and ``error=False`` is given.

        Raises
        ------
        OSError
            If ``error=True`` is given (default) and a token discovery
            fails.
        """
        audience = self.audience
        if audience is None and url is not None:
            audience = default_audience(url)
        try:
            return find_func(
                audience=audience,
                **discover_kwargs,
            )
        except OSError:  # failed to discover token
            if error:
                raise
            return None

    def generate_bearer_header(self, response=None):
        """Generate a bearer token header, possibly based on a response.
        """
        token = self.token
        error = response is not None or token is True
        if (
            response is not None
            or token in (None, True)
        ):
            # try and find a token
            token = self.find_token(
                url=getattr(response, "url", None),  # allow r as Session
                error=error,
            )

        # if we ended up with a token, generate the header content
        if token:
            return self._auth_header_str(token)

    def authenticate_bearer(self, response, **kwargs):
        """Re-send a request in response to a Bearer challenge.
        """
        try:
            auth_header = self.generate_bearer_header(response)
        except ValueError:
            # return original response
            return response

        # consume the content so that we can reuse the connection
        response.content
        response.raw.release_conn()

        # retry the same request, using the same connection
        request = response.request.copy()
        request.headers["Authorization"] = auth_header
        new = response.connection.send(request, **kwargs)
        new.history.append(response)
        return new

    def handle_401(self, response, **kwargs):
        """Handle 401 response.
        """
        params = _www_authenticate_bearer_params(response)
        if isinstance(params, dict):
            kwargs.update(params)
            return self.authenticate_bearer(response, **kwargs)
        return response

    def handle_response(self, response, **kwargs):
        """Attempt to handle a response that asks for Bearer auth.
        """
        num_401s = kwargs.pop("num_401s", 0)
        if response.status_code == 401 and num_401s < 2:
            new = self.handle_401(response, **kwargs)
            num_401s += 1
            return self.handle_response(new, num_401s=num_401s, **kwargs)

        return response

    def __call__(self, request):
        """Augment the `Request` ``request`` with an ``Authorization`` header.
        """
        token = self.token
        if self.force:
            # try and find a token
            token = self.find_token(
                url=request.url,
                error=True,
            )

        # if we ended up with a header, store it in the request.
        if token:
            request.headers["Authorization"] = self._auth_header_str(token)

        # register our reponse handler
        request.register_hook("response", self.handle_response)

        return request
