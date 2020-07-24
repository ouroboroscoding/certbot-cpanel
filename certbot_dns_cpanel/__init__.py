"""
The `~certbot_dns_cpanel.dns_cpanel` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the cPanel ZoneEdit module in API 2.

Named Arguments
---------------

========================================  =====================================
``--dns-cpanel-propagation-seconds``      The number of seconds to wait for DNS
                                          to propagate before asking the ACME
                                          server to verify the DNS record.
                                          (Default: 10)
========================================  =====================================

Credentials
-----------
Use of this plugin requires a configuration file containing cPanel API
credentials for an account with ZoneEdit permissions. The file should be found
at ~/.cpanel/config and be a JSON formatted object with "domain", "user", and
"token" keys

Examples
--------
.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``

   certbot certonly \\
     --dns-cpanel \\
     -d example.com

.. code-block:: bash
   :caption: To acquire a single certificate for both ``example.com`` and
             ``www.example.com``

   certbot certonly \\
     --dns-cpanel \\
     -d example.com \\
     -d www.example.com

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``, waiting 30 seconds
             for DNS propagation

   certbot certonly \\
     --dns-cpanel \\
     --dns-cpanel-propagation-seconds 30 \\
     -d example.com
"""
