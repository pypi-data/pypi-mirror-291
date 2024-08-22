"""A CPSMS gateway."""

import base64
import getopt
from http.client import HTTPResponse
import json
import re
from urllib import error, parse, request
from typing import Any, Dict, Optional, Tuple


class Gateway:
    """
    A Python wrapper around the SMS gateway from CPSMS <https://www.cpsms.dk/>.

    Please look at the README for further description.
    """

    options: Dict[str, Any] = {}
    username: str
    password: str
    gateway_base_url: str = "https://api.cpsms.dk"

    @property
    def default_options(self) -> Dict[str, Any]:
        """Get some default options to use."""
        return {
            "to": "",
            "message": "",
            "from": "",
            "timestamp": "",  # For delaying messages. Format: Unix timestamp.
            "encoding": "UTF-8",
            "dlr_url": "",
            "flash": False,
            "reference": "",
            "format": "GSM",
        }

    def __init__(
        self,
        username: str,
        password: str,
        sender_name: str,
        options: Dict[str, Any] = None,
        gateway_base_url: str = None,
    ) -> None:
        """Initialize SMS gateway."""
        self.username = username
        self.password = password

        self.options = self.default_options
        self.options["from"] = sender_name

        if options is not None:
            self.options.update(options)

        if gateway_base_url:
            self.gateway_base_url = gateway_base_url

    def request(self, path: str, data: Optional[dict] = None) -> dict:
        """Make a request to the gateway and return the response data."""
        # Construct the authentication header.
        auth_header = "{}:{}".format(self.username, self.password)
        auth_header = base64.b64encode(auth_header.encode()).decode()

        # Prepare and make the request.
        http_request = request.Request(self.gateway_base_url + path, data=data)
        http_request.add_header("Authorization", "Basic {}".format(auth_header))
        response = request.urlopen(http_request)

        # Parse and return the response data.
        return json.loads(response.read().decode())

    def send(self, to: str = None, message: str = None) -> Tuple[bool, str]:
        """
        Send a message to a recipient.

        Optionally, override the recpient and the message to be sent.
        """
        # Raise an error if the sender is not specified.
        if not self.options["from"]:
            raise ValueError("Sender name cannot be empty.")
        # Update message if specified.
        if message is not None:
            self.options["message"] = message

        # Raise error if message is empty.
        if not self.options["message"]:
            raise ValueError("Message cannot be empty.")

        # Raise error if message is too long.
        if len(self.options["message"]) > 459:
            raise ValueError(
                "Message not allowed to be more than 459 characters."
                "Current message is %i characters." % len(self.options["message"])
            )

        # Update recipient if specified.
        if to is not None:
            self.options["to"] = to

        # Raise error if recipients is empty.
        if not self.options["to"]:
            raise ValueError("No recipient is set.")

        # Raise error if recipient is not a number.
        pattern = re.compile("^[0-9]+$")
        if pattern.match(self.options["to"]) is None:
            raise ValueError(
                "Recipient number must be numbers only (no characters, spaces or +)"
            )

        # Prepare the data to send along.
        options = self.options
        options["flash"] = int(options["flash"])
        data = json.dumps(options).encode()

        return self.request("/v2/send", data=data)

    def get_credit_status(self) -> float:
        """Get the credit status."""
        # As the amount is returned as a string with a Danish decimal
        # separator, we replace this before parsing the amount.
        data = self.request("/v2/creditvalue")
        amount = float(data["credit"].replace(",", "."))

        return amount
