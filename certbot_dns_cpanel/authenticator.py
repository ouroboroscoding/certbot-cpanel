# coding=utf8
"""Certbot cPanel DNS Authenticator

Sets up certbot checking via cPanel DNS interface
"""

__author__		= "Chris Nasr"
__copyright__	= "OuroborosCoding"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "ouroboroscode@gmail.com"
__created__		= "2020-07-23"

# Python imports
import collections
import json

# Pip imports
from acme.magic_typing import DefaultDict
from acme.magic_typing import Dict
from acme.magic_typing import List
from certbot import errors
from certbot import interfaces
from certbot.compat import os
from certbot.plugins import dns_common
import zope.interface

# Local imports
from .cpanel_apiv2 import API

INSTRUCTIONS = (
	'To use certbot-cpanel configure credentials in ~/.cpanel/config. The file '
	'should be a JSON formatted object with "domain", "user", and "token" keys'
)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
	"""Authenticator

	Used to fulfill dns-01 challenge
	"""

	description = ("Obtain certificates using a DNS TXT record (if you are using cPanel ZoneEdit for DNS).")
	ttl = 10

	def __init__(self, *args, **kwargs):
		"""Constructor

		Initialises the instance

		Returns:
			Authenticator
		"""

		super(Authenticator, self).__init__(*args, **kwargs)
		self._resource_records = collections.defaultdict(list) # type: DefaultDict[str, List[Dict[str, str]]]

		# Figure out the path to the config
		path = os.path.expanduser('~/.cpanel')

		# Try
		try:

			# Open the file
			with open('%s/config' % path) as f:
				dConf = json.load(f, encoding='utf8')

			# Create the api instance
			self._api = API(**dConf)

		# Catch any exception as we can't continue with any errors
		except Exception as e:
			raise errors.PluginError("\n".join([str(e), INSTRUCTIONS]))

	def more_info(self):
		"""More Info

		Describes the plugin"""

		return "Solve a DNS01 challenge using cPanel ZoneEdit"

	def _setup_credentials(self):
		pass

	def _perform(self, domain, validation_name, validation):
		"""Perform

		Creates the records needed for verification"""
		print('_perform(%s, %s, %s)' % (
			domain, validation_name, validation
		))

		# Split the domain by period and only keep the last two parts
		sDomain = '.'.join(domain.split('.')[-2:])
		iDomain = len(sDomain)

		# Fetch the existing zones from cPanel
		mRes = self._api.fetchZoneRecords(
			sDomain,
			name='%s.' % validation_name,
			type_='TXT'
		)

		# If we got a string back
		if isinstance(mRes, str):
			raise errors.PluginError(mRes)

		# If there's no record
		if not mRes:

			# Create new record
			print('Creating record %s' % validation_name)
			sRes = self._api.addZoneRecord(
				sDomain,
				name='%s.' % validation_name,
				data=validation,
				ttl=self.ttl
			)
			if sRes:
				raise errors.PluginError(sRes)

		# Else the record exists
		else:

			# If the values are different
			if mRes['txtdata'] != validation:

				# Update existing record
				print('Updating record %s' % validation_name)
				sRes = self._api.editZoneRecord(
					sDomain,
					name='%s.' % validation_name,
					data=validation,
					line=mRes['line'],
					ttl=self.ttl
				)
				if sRes:
					raise errors.PluginError(sRes)

	def _cleanup(self, domain, validation_name, validation):
		"""Cleanup

		Removes records made in perform"""

		# Get the data from cPanel

		print('_cleanup(%s, %s, %s)' % (
			domain, validation_name, validation
		))

		# Split the domain by period and only keep the last two parts
		sDomain = '.'.join(domain.split('.')[-2:])

		# Fetch the existing zones from cPanel
		mRes = self._api.fetchZoneRecords(
			sDomain,
			name='%s.' % validation_name,
			type_='TXT'
		)

		# If we got a string back
		if isinstance(mRes, str):
			raise errors.PluginError(mRes)

		# Delete the record
		print('Removing record %s' % validation_name)
		sRes = self._api.removeZoneRecord(
			sDomain,
			line=mRes['line']
		)
		if sRes:
			raise errors.PluginError(sRes)

