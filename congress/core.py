import os
from datetime import datetime
from datetime import timedelta
from warnings import warn

import requests


class Congress():
    """Python wrapper class implementing a client for Congress.gov API.
    For documentation, see:
    https://api.congress.gov/#/bill
    https://github.com/LibraryOfCongress/api.congress.gov/

    Returns:
        Congress: object
    """

    # How far back in time from today should the API search?
    NOW = datetime.now()
    CURRENT_DATE_OFFSET = timedelta(days=365*20)  # roughly 20 years
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    __origin_url = "https://api.congress.gov/v3"
    token_param_name = "api_key"

    def __init__(self, api_key=None):

        # Get API Key
        if api_key:
            self.__api_key = api_key
        else:
            try:
                self.__api_key = os.environ["CONGRESS_API_KEY"]
            except KeyError:
                print("Congress API Key not found")
                raise

        # Initialize default query parameters
        self.__default_query_params = {
            "format": "json",
            "offset": 0,
            "limit": 25,
            "fromDateTime": (self.NOW - self.CURRENT_DATE_OFFSET).strftime(self.DATETIME_FORMAT),
            "toDateTime": self.NOW.strftime(self.DATETIME_FORMAT),
            "sort": "updateDate+desc",
        }

    def __send_request(self, full_url, **kwargs):
        """Send a get request to the specified congress API endpoint, with the provided parameters.

        Args:
            full_url (str): Congress API endpoint

        Raises:
            ValueError: If get request is unsuccessful

        Returns:
            response (requests.Response): The response object
        """

        kwargs[self.token_param_name] = self.__api_key
        response = requests.get(full_url, params=kwargs)
        if not response.ok:
            raise ValueError("Bad request")
        else:
            return response

    def __validate_params(self, params):
        """Validate get request parameter values

        Args:
            params (dict): User-specified parameter names and values to be propagated to
            __send_request()

        Returns:
            query_params (dict): Validated parameter names and values to be propagated to
            __send_request()
        """

        # Initialize request parameters as default parameters
        query_params = self.__default_query_params

        # Replace request parameters with user-supplied parameters
        for param in params:
            if param in query_params:
                query_params[param] = params[param]
            else:
                warn(f"Invalid parameter name '{param}' supplied.\
                    Will use default name and value instead.")
        return query_params

    def __compose_full_url(self, url_prefix, path):
        """Compose full URL to be propagated to __send_request()

        Args:
            url_prefix (str): Root of desired Congress API endpoint
            path (str): Path of desired Congress API endpoint, not including the root

        Returns:
            str: Full path of desired Congress API endpoint (i.e including the root)
        """

        if not path:
            path = ""
        full_url = '/'.join([self.__origin_url, url_prefix, path])
        return full_url

    def __process_request(self, url_prefix, path, params):
        """Processes requests to the Congress API. First validates the user-specified
        parameters, then composes a full URL of the endpoint, and finally sends the request to
        (and receives the response from) the Congress API.

        Args:
            url_prefix (str): Root of desired Congress API endpoint
            path (str): Path of desired Congress API endpoint, not including the root
            params (dict): User-specified parameter names and values to be propagated to
            __send_request()

        Returns:
            response (requests.Response): The response object
        """

        query_params = self.__validate_params(params)
        full_url = self.__compose_full_url(url_prefix, path)
        response = self.__send_request(full_url, **query_params)
        return response

    def bill(self, path=None, **params):
        """Implements access to all '/bill/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("bill", path, params)
        return response.text

    def amendment(self, path=None, **params):
        """Implements access to all '/amendment/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("amendment", path, params)
        return response.text

    def summaries(self, path=None, **params):
        """Implements access to all '/summaries/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("summaries", path, params)
        return response.text

    def congress(self, path=None, **params):
        """Implements access to all '/congress/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("congress", path, params)
        return response.text

    def member(self, path=None, **params):
        """Implements access to all '/member/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("member", path, params)
        return response.text

    def committee(self, path=None, **params):
        """Implements access to all '/committee/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee", path, params)
        return response.text

    def committee_report(self, path=None, **params):
        """Implements access to all '/committee-report/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee-report", path, params)
        return response.text

    def committee_print(self, path=None, **params):
        """Implements access to all '/committee-print/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee-print", path, params)
        return response.text

    def committee_meeting(self, path=None, **params):
        """Implements access to all '/committee-meeting/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee-meeting", path, params)
        return response.text

    def hearing(self, path=None, **params):
        """Implements access to all '/hearing/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("hearing", path, params)
        return response.text

    def congressional_record(self, path=None, **params):
        """Implements access to all '/congressional-record/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("congressional-record", path, params)
        return response.text

    def daily_congressional_record(self, path=None, **params):
        """Implements access to all '/daily-congressional-record/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("daily-congressional-record", path, params)
        return response.text

    def bound_congressional_record(self, path=None, **params):
        """Implements access to all '/bill/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("bound-congressional-record", path, params)
        return response.text

    def house_communication(self, path=None, **params):
        """Implements access to all '/house-communication/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("house-communication", path, params)
        return response.text

    def house_requirement(self, path=None, **params):
        """Implements access to all '/house-requirement/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("house-requirement", path, params)
        return response.text

    def senate_communication(self, path=None, **params):
        """Implements access to all '/senate-communication/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("senate-communication", path, params)
        return response.text

    def nomination(self, path=None, **params):
        """Implements access to all '/nomination/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("nomination", path, params)
        return response.text

    def treaty(self, path=None, **params):
        """Implements access to all '/treaty/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("treaty", path, params)
        return response.text
