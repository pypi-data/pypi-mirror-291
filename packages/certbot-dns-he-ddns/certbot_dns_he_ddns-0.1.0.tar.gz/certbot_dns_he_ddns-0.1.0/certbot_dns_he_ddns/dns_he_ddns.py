import logging

import requests
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """
    Dynamic DNS Authenticator for Hurrican Electric
    """

    description = "Obtain certificates using a DNS TXT record (using Hurricane Electric with dynamic TXT records)."

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add)
        add("credentials", help="Hurricane Electric credentials INI file.")

    def more_info(self):
        return "This plugin configures a pre-existing dynamic TXT record to respond to a dns-01 challenge using the Hurricane Electric dynamic DNS API."

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Hurricane Electric dynamic DNS credentials INI file",
            {
                "password": "Password for the dynamic TXT record",
            },
        )

    def _perform(self, domain, validation_name, validation):
        logger.info("Updating TXT record for %s (%s)", validation_name, domain)
        self._client().update_txt_record(validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        logger.info("Clearing TXT record for %s (%s)", validation_name, domain)
        self._client().clear_txt_record(validation_name)

    def _client(self):
        return HEDDNSClient(self.credentials.conf("password"))


class HEDDNSClient(object):
    BASE = "https://dyn.dns.he.net"

    def __init__(self, password):
        self.password = password
        self.session = requests.Session()

    def _update(self, hostname, txt):
        data = {
            "hostname": hostname,  # _acme-challenge.mydomain.com
            "password": self.password,
            "txt": txt,
        }
        resp = self.session.post(self.BASE + "/nic/update", data=data)
        if resp.status_code != 200:
            raise errors.PluginError(
                "Bad HTTP status posting update {0}: {1}".format(
                    resp.status_code, resp.text
                )
            )

        if "good" in resp.text:
            return
        elif "nochg" in resp.text:
            # The value has already been set, no change needed.
            return
        elif "badauth" in resp.text:
            raise errors.PluginError("Bad authentication")
        elif "badtxt" in resp.text:
            raise errors.PluginError("Bad TXT record")
        elif "abuse" in resp.text:
            raise errors.PluginError("Abuse detected")
        else:
            raise errors.PluginError("Unknown API response: {0}".format(resp.text))

    def update_txt_record(self, record_name, content):
        """
        Update the content of the TXT record.
        """
        return self._update(record_name, content)

    def clear_txt_record(self, record_name):
        """
        Clear the content of the TXT record.
        """
        return self._update(record_name, '""')
