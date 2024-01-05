# Congress
Python wrapper of the US Congress API, used for retrieving data on the dealings of the United States Congress. They expose endpoints that provide data on legislation, meetings, hearings, treaties, and members of Congress, amongst others.

* For full list of endpoints, see https://api.congress.gov
* For full API documentation, see https://github.com/LibraryOfCongress/api.congress.gov

This Python client allows a user to initialize a `Congress` object with their `api_key` and use it to access and collect information from the Congress API. The API responses are passed on directly to the user as delivered from the server, allowing the user to implement further custom dowstream processing.

# Getting setup
1. Apply for an api key from Congress.gov [here](https://api.congress.gov/sign-up/).
2. Download this repo or `git clone` it to your local directory of choice
3. Optional: Save your api key to your environment by adding the line `export CONGRESS_API_KEY=<your API key from step 1>` to your shell's `profile` document. Then simply call `Congress()` in your python IDE.

# Overview

```python
>>> import congress

# Initialize Congress object
# with API key
>>> client = Congress(api_key = my_API_key_from_step_1)

# Or without (if you did Step 3 above)
>>> client = Congress()

# Access bill endpoints
#-------------------------

# Access bill endpoint: '/bill'
>>> client.bill()

# Access bill endpoint: '/bill/{congress}/{billType}'
>>> congress, billType = 117, 'hr'

>>> client.bill(f'{congress}/{billType}')

# and so on...

# Access amendment endpoints
#---------------------------

# Access amendment endpoint: '/amendment'
>>> client.amendment()

# Access amendment endpoint: '/amendment/{congress}/{amendmentType}/{amendmentNumber}/cosponsors'
>>> congress, amendmentType, amendmentNumber = 117, 'samdt', 2137

>>> client.amendment(f'{congress}/{amendmentType}/{amendmentNumber}/cosponsors')

# and so on...
```

Similar methods exist for all other endpoints on the Congress API, replacing the occasional hyphen `-` with underscore `_`

```python
>>> client.summaries()

>>> client.congress()

>>> client.member()

>>> client.committee()

>>> client.committee_report()

>>> client.committee_print()

>>> client.committee_meeting()

>>> client.hearing()

>>> client.congressional_record()

>>> client.daily_congressional_record()

>>> client.bound_congressional_record()

>>> client.house_communication()

>>> client.house_requirement()

>>> client.senate_communication()

>>> client.nomination()

>>> client.treaty()
```

Note that you can also pass query parameters as kwargs to send to the Congress API (see their documentation), for example

```python
# Return data as XML instead of JSON
client.bill(f'{congress}/{billType}', format='xml')
```


