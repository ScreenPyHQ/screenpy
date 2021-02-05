"""
An ability that will allow the actor to make API requests and store the
responses.
"""

from typing import Any, Callable, Dict, List, Optional

from requests import Response, Session

from ..exceptions import RequestError


class MakeAPIRequests:
    """The ability to send API requests.

    Examples::

        Perry = AnActor.named("Perry").who_can(MakeAPIRequests())

        Perry = AnActor.named("Perry").who_can(
            MakeAPIRequests.using(session_instance)
        )
    """

    @staticmethod
    def using(session: Session) -> "MakeAPIRequests":
        """Provide a |Requests| session for the ability to use."""
        return MakeAPIRequests(session=session)

    def to_send(self, method: str, url: str, **kwargs: Any) -> None:
        """
        Send a request. This is a pass-through to the session's ``request``
        method and has the same signature. The response is stored in the
        responses list in this ability.

        Args:
            method: the HTTP method of the request - GET, POST, etc.
            url: the URL to which to send the request.
            kwargs: additional keyword arguments to pass through to |request|.
        """
        http_requests: Dict[str, Callable] = {
            "DELETE": self.session.delete,
            "GET": self.session.get,
            "HEAD": self.session.head,
            "OPTIONS": self.session.options,
            "PATCH": self.session.patch,
            "POST": self.session.post,
            "PUT": self.session.put,
        }
        method = method.upper()

        if method not in http_requests:
            raise RequestError(f'"{method}" is not a valid HTTP method.')

        self.responses.append(http_requests[method](url, **kwargs))

    send = to_send

    def forget(self) -> None:
        """Clean up the Session instance stored in this ability."""
        self.session.close()

    def __repr__(self) -> str:
        return "Make API Requests"

    __str__ = __repr__

    def __init__(self, session: Optional[Session] = None) -> None:
        if session is None:
            session = Session()
        self.session = session
        self.responses: List[Response] = []
