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

	def addZoneRecord(self, domain, name, data, ttl=900):
		"""Add Zone Record

		Adds a new record to the domain's zone

		Arguments:
			domain (str): The domain to add to
			name (str): The record to add
			data (str): The data associated with the record

		Returns:
			None
		"""

		# Create headers
		dHeaders = {
			"Authorization": self.__generateAuth()
		}

		# Generate the URL
		sURL = self.__generateURL('ZoneEdit', 'add_zone_record', {
			"domain": domain,
			"name": name,
			"type": 'TXT',
			"txtdata": data,
			"ttl": ttl
		})

		# Make the request
		oRes = requests.get(sURL, headers=dHeaders)

		# Get the data
		dRes = oRes.json()

		# If we didn't get 200
		if oRes.status_code != 200:
			return dRes['cpanelresult']['error']

		# Else if we got a status message
		if 'statusmsg' in dRes['cpanelresult']['data']:
			return dRes['cpanelresult']['data']['statusmsg']

		# Return ok
		return ''

	def editZoneRecord(self, domain, name, data, line, ttl=900):
		"""Edit Zone Record

		Updates an existing record to the domain's zone

		Arguments:
			domain (str): The domain to add to
			name (str): The record to add
			data (str): The data associated with the record
			line (uint): The line to replace

		Returns:
			str: error message
		"""

		# Create headers
		dHeaders = {
			"Authorization": self.__generateAuth()
		}

		# Generate the URL
		sURL = self.__generateURL('ZoneEdit', 'edit_zone_record', {
			"line": line,
			"domain": domain,
			"name": name,
			"type": 'TXT',
			"txtdata": data,
			"ttl": ttl
		})

		# Make the request
		oRes = requests.get(sURL, headers=dHeaders)

		# Get the data
		dRes = oRes.json()

		# If we didn't get 200
		if oRes.status_code != 200:
			return dRes['cpanelresult']['error']

		# Else if we got a status message
		if 'statusmsg' in dRes['cpanelresult']['data']:
			return dRes['cpanelresult']['data']['statusmsg']

		# Return ok
		return ''

	def fetchZoneRecords(self, domain, name=None, type_=None):
		"""Fetch Zone Records

		Fetches records for a specific domain

		Arguments:
			domain (str): The domain to fetch records for
			name (str): Optional name to fetch a specific record
			type_ (str): The type of record to return

		Returns:
			list|dict|None
		"""

		# Create headers
		dHeaders = {
			"Authorization": self.__generateAuth()
		}

		# Generate params
		dQuery = {"domain": domain}
		if name: dQuery['name'] = name
		if type_: dQuery['type'] = type_

		# Generate the URL
		sURL = self.__generateURL('ZoneEdit', 'fetchzone_records', dQuery)

		# Make the request
		oRes = requests.get(sURL, headers=dHeaders)

		# Get the data
		dRes = oRes.json()

		# If we didn't get 200
		if oRes.status_code != 200:
			return dRes['cpanelresult']['error']

		# Else if we got a status message
		if 'statusmsg' in dRes['cpanelresult']['data']:
			return dRes['cpanelresult']['data']['statusmsg']

		# If there's a name
		if name:
			return dRes['cpanelresult']['data'] and dRes['cpanelresult']['data'][0] or None

		# Return the records
		return dRes['cpanelresult']['data']

	def removeZoneRecord(self, domain, line):
		"""Remove Zone Record

		Removes an existing record from the domain's zone

		Arguments:
			domain (str): The domain to add to
			line (uint): The line to replace

		Returns:
			None
		"""

		# Create headers
		dHeaders = {
			"Authorization": self.__generateAuth()
		}

		# Generate the URL
		sURL = self.__generateURL('ZoneEdit', 'remove_zone_record', {
			"line": line,
			"domain": domain
		})

		# Make the request
		oRes = requests.get(sURL, headers=dHeaders)

		# Get the data
		dRes = oRes.json()

		# If we didn't get 200
		if oRes.status_code != 200:
			return dRes['cpanelresult']['error']

		# Else if we got a status message
		if 'statusmsg' in dRes['cpanelresult']['data']:
			return dRes['cpanelresult']['data']['statusmsg']

		# Return ok
		return ''
