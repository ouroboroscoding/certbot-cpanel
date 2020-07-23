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
import json

# Pip imports
from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot.compat import os
import zope.interface

# Local imports
from .cpanel_apiv2 import API

INSTRUCTIONS = (
	'To use certbot-cpanel configure credentials in ~/.cpanel/config. The file ' \
	'should be a JSON formatted object with "host", "user", and "token" keys'
)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
	"""Authenticator

	Used to fulfill dns-01 challenge
	"""

	description = ("Obtain certificates using a DNS TXT record (if you are using cPanel ZoneEdit for DNS).")

	def __init__(self, *args, **kwargs):
		"""Constructor

		Initialises the instance

		Returns:
			Authenticator
		"""

		# Call parent
		super(Authenticator, self).__init__(*args, **kwargs)

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

	def _cleanup(self, domain, validation_name, validation):
		"""Cleanup

		Removes records made in perform"""

		# Get the data from cPanel

		print('_cleanup(%s, %s, %s)' % (
			domain, validation_name, validation
		))

