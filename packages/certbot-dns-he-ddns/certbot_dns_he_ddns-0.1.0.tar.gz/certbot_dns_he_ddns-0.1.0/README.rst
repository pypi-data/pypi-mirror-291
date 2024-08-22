cerbot-dns-he-ddns
======================================

`Hurricane Electric dynamic DNS <https://dns.he.net>`_ Authenticator
plugin for `Certbot <https://certbot.eff.org>`_.

This plugin automates the process of completing a ``dns-01`` challenge
by updating, and subsequently clearing, TXT records using the
`Hurricane Electric dynamic DNS API <https://dns.he.net/docs.html>`_.

This method allows limiting access to specific records.

----

Installation
------------

::

    pip install certbot-dns-he-ddns

Alternatively, you can use
``git+https://github.com/mafredri/certbot-dns-he-ddns.git``.

Preparation
-----------

This plugin can only complete challenges for pre-existing
``_acme-challenge.*`` DNS records that are of the ``TXT`` type and have
the dynamic DNS feature enabled. To configure multiple domains they must
share the same password.

1. Add a new ``TXT`` record:

   - Name: ``_acme-challenge.example.com``
   - Text data: ``empty``
   - TTL: 300
   - *Enable entry for dynamic DNS* must be checked.

2. Set the dynamic DNS key for the new record by pressing 🔃, it should
   match the password configured for this plugin.

Credentials
-----------

An example ``credentials.ini`` file:

.. code-block:: ini

   dns_he_ddns_password = verysecurepassword

Examples
--------

To acquire a single certificate for both ``example.com`` and
``*.example.com``, waiting 60 seconds for DNS propagation:

.. code-block:: bash

   certbot certonly \
     --authenticator dns-he-ddns \
     --dns-he-ddns-credentials /etc/letsencrypt/.secrets/dns-he-ddns.ini \
     --dns-he-ddns-propagation-seconds 60 \
     --server https://acme-v02.api.letsencrypt.org/directory \
     --preferred-challenges dns \
     --agree-tos \
     --rsa-key-size 4096 \
     -d 'example.com' \
     -d '*.example.com'
