"""
This module aims to detect a site which is trying to phish you, focusing on
the identity of the owner of the site which is being presented to you.

Definitions:
    1. Owner: the owner of the site is the actual owner you expect
    2. Masquerader: the entity which is pretending to be the owner of the
        content, and different from the owner of the phishing site.

Outline of approach:
    * We try to establish who an average user would think the owner of the
      site is by:
        * taking a screenshot of the site
        * detecting the logos on the site from the screenshot
        * determining if the site belongs to any of those entities
    * Checking information in the SSL cert
        * is there a cert?
        * is the issuer someone who we think should be the owner?
    * Checking URL
        * is the url on a domain that belongs to the proposed Owner

Needs some fleshing out of how to compare urls and cert owners,
maybe fuzzy searching.
"""

from urllib.parse import urlparse

from cert_detection import get_cert_entities
from screenshits import ScreenShit


def main():
    # take screenshit of site, very basic
    # url = "https://hibshman.net"
    url = "http://nyuclubs.atspace.cc/"
    screenshit = ScreenShit(url=url)

    parsed_hostname = "{}".format(urlparse(url).netloc)

    if not parsed_hostname:
        raise ValueError("Please enter url in correct format")

    screenshit.capture_and_save_as(
        "{}.jpeg".format(parsed_hostname)
    )

    # TODO: send for logo detection once I have the logograb keys
    # if that takes a while I will try out Google's

    # SSL cert info
    cert_info = get_cert_entities(url)

    if not any(cert_info.values()):
        print(
            "No SSL cert found for <{}>, "
            "GTFO and contact your site adminitstrator"
            .format(parsed_hostname)
        )
    else:
        # TODO: compare this to the brand we think is the owner, based on
        # logo detection
        print(
            "SSL Certificate issued to <{}> by <{}>".format(
                cert_info['issued_to'],
                cert_info['issued_by']
            )
        )

    # TODO: url fuzzy matching


main()
