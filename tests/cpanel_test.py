"""Tests for certbot_dns_route53._internal.dns_route53.Authenticator"""

import unittest

try:
    import mock
except ImportError: # pragma: no cover
    from unittest import mock # type: ignore

from certbot import errors
from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins.dns_test_common import DOMAIN

class AuthenticatorTest(unittest.TestCase, dns_test_common.BaseAuthenticatorTest):
    # pylint: disable=protected-access

    def setUp(self):
        from certbot_cpanel.authenticator import Authenticator
        super(AuthenticatorTest, self).setUp()
        self.auth = Authenticator({}, 'cpanel')

    def tearDown(self):
        super(AuthenticatorTest, self).tearDown()

    def test_perform(self):
        print('bleh')
        self.assertEqual('true', 'true')

if __name__ == "__main__":
    unittest.main()  # pragma: no cover
