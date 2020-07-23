# coding=utf8
""" API

Uses the JSON api to access functions in cPanel setups
"""

__author__		= "Chris Nasr"
__copyright__	= "OuroborosCoding"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "ouroboroscode@gmail.com"
__created__		= "2020-07-23"

# Python imports
import base64
import urllib.parse

# Pip imports
import requests

class API(object):
	"""API

	Class to hold information related to the connection
	"""

	def __init__(self, domain, user, token):
		"""Constructor

		Handles creating the instance of the class

		Arguments:
			domain (str): The domain name of the domain
			user (str): The user used to sign in
			passwd (str): The password associated with the user

		Returns:
			API
		"""

		# Store the values
		self._domain = domain
		self._user = user
		self._token = token

	def __generateAuth(self):
		"""Generate Auth

		Uses the stored user/pass to generate an authorization token

		Returns:
			str
		"""

		# Return the header string
		return 'cpanel %s:%s' % (
			self._user,
			self._token
		)

	def __generateURL(self, module, function, params={}):
		"""Generate URL

		Takes a path and params and generates the full URL with query string

		Arguments:
			module (str): The module to use
			function (str): The function in the module
			params (dict): Name/value query pairs

		Returns:
			str
		"""

		# Add to params
		params['cpanel_jsonapi_module'] = module
		params['cpanel_jsonapi_func'] = function
		params['cpanel_jsonapi_version'] = 2

		# Generate and return the URL
		return 'https://%s:2083/json-api/cpanel?%s' % (
			self._domain,
			urllib.parse.urlencode(params)
		)

	def fetchZone(self, domain):
		"""Fetch Zone

		Fetches records for a specific domain

		Arguments:
			domain (str): The domain to fetch records for

		Returns:
			list
		"""

		# Create headers
		dHeaders = {
			"Authorization": self.__generateAuth()
		}

		print(dHeaders)

		# Generate the URL
		sURL = self.__generateURL('ZoneEdit', 'fetchzone', {
			"domain": domain
		})

		print(sURL)

		# Make the request
		oRes = requests.get(sURL, headers=dHeaders)

		# Get the data
		dRet = oRes.json()

		# If we didn't get 200
		if oRes.status_code != 200:
			print(dRet['cpanelresult']['error'])
			return None

		# Return the data
		return dRet['cpanelresult']['data']
