import os
from time import sleep
from datetime import datetime, timedelta
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

    FIRST_REQUEST_TIMESTAMP = None
    CURRENT_DATE_OFFSET = timedelta(days=365*20)  # API searches roughly 20 years from today
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    REQUEST_COUNT = 0

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
            "fromDateTime": (
                datetime.now() - self.CURRENT_DATE_OFFSET
            ).strftime(self.DATETIME_FORMAT),
            "toDateTime": datetime.now().strftime(self.DATETIME_FORMAT),
            "sort": "updateDate+desc",
        }

    def __throttle(self):
        rq_pace_limit = 1000/3600  # Rate limit (1000 requests per hour) in rq/seconds
        time_delta_secs = (datetime.now() - Congress.FIRST_REQUEST_TIMESTAMP)
        request_pace = Congress.REQUEST_COUNT / time_delta_secs.total_seconds()

        if request_pace >= rq_pace_limit:
            print("Throttling...")
            # print(f"Current pace of requests ({request_pace * 3600} per hour) too high. Throttling...")  # noqa: E501
            # Calculate delay
            delay = timedelta(
                seconds=((Congress.REQUEST_COUNT + 1)/rq_pace_limit)
            ) - time_delta_secs
            delay = delay.total_seconds()  # convert to seconds
        else:
            delay = 0

        sleep(delay)

    def __send_request(self, full_url, throttle, **kwargs):
        """Send a get request to the specified congress API endpoint, with the provided parameters.

        Args:
            full_url (str): Congress API endpoint

        Raises:
            ValueError: If get request is unsuccessful

        Returns:
            response (requests.Response): The response object
        """
        # Store time of first request persistently for throttling
        if Congress.FIRST_REQUEST_TIMESTAMP is None:
            Congress.FIRST_REQUEST_TIMESTAMP = datetime.now()

        if Congress.REQUEST_COUNT > 1:
            if throttle:
                self.__throttle()

        kwargs[self.token_param_name] = self.__api_key
        response = requests.get(full_url, params=kwargs)
        Congress.REQUEST_COUNT += 1

        # Try again 3 times if request is unsuccessful
        while_count = 0
        while (response.status_code != 200) and (while_count < 3):
            sleep(0.5)  # rest for a bit
            response = requests.get(full_url, params=kwargs)
            Congress.REQUEST_COUNT += 1
            while_count += 1

        if response.status_code != 200:
            raise ValueError(f"Bad request; API responded with status code {response.status_code}")
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
        full_url = '/'.join([self.__origin_url, url_prefix, path.lower()])
        return full_url

    def __process_request(self, url_prefix, path, throttle, params):
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
        response = self.__send_request(full_url, throttle, **query_params)
        return response

    def bill(self, path=None, throttle=False, **params):
        """Implements access to all '/bill/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("bill", path, throttle, params)
        return response.text

    def amendment(self, path=None, throttle=False, **params):
        """Implements access to all '/amendment/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("amendment", path, throttle, params)
        return response.text

    def summaries(self, path=None, throttle=False, **params):
        """Implements access to all '/summaries/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("summaries", path, throttle, params)
        return response.text

    def congress(self, path=None, throttle=False, **params):
        """Implements access to all '/congress/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("congress", path, throttle, params)
        return response.text

    def member(self, path=None, throttle=False, **params):
        """Implements access to all '/member/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("member", path, throttle, params)
        return response.text

    def committee(self, path=None, throttle=False, **params):
        """Implements access to all '/committee/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee", path, throttle, params)
        return response.text

    def committee_report(self, path=None, throttle=False, **params):
        """Implements access to all '/committee-report/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee-report", path, throttle, params)
        return response.text

    def committee_print(self, path=None, throttle=False, **params):
        """Implements access to all '/committee-print/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee-print", path, throttle, params)
        return response.text

    def committee_meeting(self, path=None, throttle=False, **params):
        """Implements access to all '/committee-meeting/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("committee-meeting", path, throttle, params)
        return response.text

    def hearing(self, path=None, throttle=False, **params):
        """Implements access to all '/hearing/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("hearing", path, throttle, params)
        return response.text

    def congressional_record(self, path=None, throttle=False, **params):
        """Implements access to all '/congressional-record/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("congressional-record", path, throttle, params)
        return response.text

    def daily_congressional_record(self, path=None, throttle=False, **params):
        """Implements access to all '/daily-congressional-record/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("daily-congressional-record", path, throttle, params)
        return response.text

    def bound_congressional_record(self, path=None, throttle=False, **params):
        """Implements access to all '/bill/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("bound-congressional-record", path, throttle, params)
        return response.text

    def house_communication(self, path=None, throttle=False, **params):
        """Implements access to all '/house-communication/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("house-communication", path, throttle, params)
        return response.text

    def house_requirement(self, path=None, throttle=False, **params):
        """Implements access to all '/house-requirement/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("house-requirement", path, throttle, params)
        return response.text

    def senate_communication(self, path=None, throttle=False, **params):
        """Implements access to all '/senate-communication/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("senate-communication", path, throttle, params)
        return response.text

    def nomination(self, path=None, throttle=False, **params):
        """Implements access to all '/nomination/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("nomination", path, throttle, params)
        return response.text

    def treaty(self, path=None, throttle=False, **params):
        """Implements access to all '/treaty/...' endpoints of the Congress API

        Args:
            path (str, optional): Endpoint URL, not including the root. Defaults to None.

        Returns:
            str (requests.Response.text): Contents of response text
        """

        response = self.__process_request("treaty", path, throttle, params)
        return response.text
