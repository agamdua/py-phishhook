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

from fuzzywuzzy import fuzz
from tabulate import tabulate

from cert_detection import get_cert_entities
from logo_detection import LogoDetection
from screenshits import ScreenShit


def main():
    # take screenshit of site, very basic
    # url = "https://hibshman.net"
    # url = "http://nyuclubs.atspace.cc/"
    # url = "https://engineering.nyu.edu"
    url = "https://www.nyu.edu"

    print("\nAnalyzing URL: <{}>".format(url))
    screenshit = ScreenShit(url=url)

    parsed_hostname = "{}".format(urlparse(url).netloc)

    if not parsed_hostname:
        raise ValueError("Please enter url in correct format")

    saved_fname = "{}.jpeg".format(parsed_hostname)

    screenshit.capture_and_save_as(saved_fname)

    # TODO: send for logo detection once I have the logograb keys
    # if that takes a while I will try out Google's

    with open(saved_fname, 'rb') as f:
        image_file = f.read()

    # brands = LogoDetection().get_brand_from_screenshot(image_file)
    brands = list(LogoDetection().get_brand_from_url(saved_fname))

    for brand in brands[:]:
        if ' ' in brand:
            splits = brand.split(' ')
            brands.append("".join([x[0] for x in splits]))

    print("Brands detected: {}".format(brands))

    # SSL cert info
    cert_info = get_cert_entities(url)

    if not any(cert_info.values()):
        print(
            "No SSL cert found for <{}>, "
            "GTFO and contact your site adminitstrator"
            .format(parsed_hostname)
        )
    else:
        print(
            "SSL Certificate issued to <{}> by <{}>\n".format(
                cert_info['issued_to']['commonName'],
                cert_info['issued_by']
            )
        )

        comparison_data = []

        comparison_list = list(cert_info['issued_to'].values())

        for brand in brands:
            for comparison_point in comparison_list:
                # naive detection for urls, only supporting up to 2 subdomains
                if len(comparison_point.split('.')) <= 4:
                    # print(
                    #     "Breaking down {} into parts".format(
                    #         comparison_point
                    #     )
                    # )

                    for item in comparison_point.split('.'):
                        match = fuzz.ratio(item.upper(), brand.upper())
                        note = "-"

                        if match > 70:
                            note = "Potential evidence that owner is legit"
                            print(
                                "========================potential match detected!=======================")  # noqa
                            print(
                                "Comparison between {} and {} = {}".format(
                                    item,
                                    brand,
                                    match,
                                )
                            )
                            print(
                                "========================================================================")  # noqa

                        comparison_data.append([item, brand, match, note])

                else:
                    match = fuzz.ratio(comparison_point.upper(), brand.upper())
                    note = "-"
                    if match > 70:
                        note = "Potential evidence that owner is legit"
                        print(
                            "========================potential match detected!=======================")  # noqa
                        print(
                            "Comparison between {} and {} = {}".format(
                                comparison_point,
                                brand,
                                match,
                            )
                        )
                        print(
                            "========================================================================")  # noqa
                    comparison_data.append([comparison_point, brand, match, note])

        print("\n\nFull Comparison Table: \n")
        print(
            tabulate(
                comparison_data,
                headers=["Item", "Brand", "Match %", "Note"]
            )
        )

main()
