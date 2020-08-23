# Python imports
from distutils.version import LooseVersion
import os
import sys

# Pip imports
from setuptools import __version__ as setuptools_version
from setuptools import setup
from setuptools.command.test import test as TestCommand

version = '1.0.1'

# Remember to update local-oldest-requirements.txt when changing the minimum
# acme/certbot version.
install_requires = [
	'requires',
	'setuptools',
	'zope.interface',
]

if not os.environ.get('EXCLUDE_CERTBOT_DEPS'):
	install_requires.extend([
		'acme>=0.29.0',
		'certbot>=1.1.0',
	])
elif 'bdist_wheel' in sys.argv[1:]:
	raise RuntimeError('Unset EXCLUDE_CERTBOT_DEPS when building wheels '
					   'to include certbot dependencies.')

setuptools_known_environment_markers = (LooseVersion(setuptools_version) >= LooseVersion('36.2'))
if setuptools_known_environment_markers:
	install_requires.append('mock ; python_version < "3.3"')
elif 'bdist_wheel' in sys.argv[1:]:
	raise RuntimeError('Error, you are trying to build certbot wheels using an old version '
					   'of setuptools. Version 36.2+ of setuptools is required.')
elif sys.version_info < (3,3):
	install_requires.append('mock')

# Test
class PyTest(TestCommand):
	user_options = []

	def initialize_options(self):
		TestCommand.initialize_options(self)
		self.pytest_args = ''

	def run_tests(self):
		import shlex
		# import here, cause outside the eggs aren't loaded
		import pytest
		errno = pytest.main(shlex.split(self.pytest_args))
		sys.exit(errno)

# Setup
setup(
	name='certbot-cpanel',
	version=version,
	description="A plugin for certbot that allows connecting to cPanel's API 2.",
	url='https://github.com/ouroboroscoding/certbot-cpanel',
	author="OuroborosCoding",
	author_email='ouroboroscode@gmail.com',
	license='Apache License 2.0',
	python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Plugins',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Security',
		'Topic :: System :: Installation/Setup',
		'Topic :: System :: Networking',
		'Topic :: System :: Systems Administration',
		'Topic :: Utilities',
	],
	packages=['certbot_dns_cpanel'],
	include_package_data=True,
	install_requires=install_requires,
	keywords=['certbot', 'dns', 'cpanel'],
	entry_points={
		'certbot.plugins': [
			'dns-cpanel = certbot_dns_cpanel.authenticator:Authenticator'
		],
	},
	tests_require=["pytest"],
	test_suite='certbot_dns_cpanel',
	cmdclass={"test": PyTest}
)
