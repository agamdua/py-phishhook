import os
import urllib

import requests

BASE_OBJECT_STORAGE_URL = "https://phish.nyc3.digitaloceanspaces.com/"


class LogoDetection:
    BASE_URL = "https://api.logograb.com/detect"

    def _construct_image_url(self, image_file):
        return "{}{}".format(BASE_OBJECT_STORAGE_URL, image_file)

    def get_brand_from_url(self, image_file):
        payload = "mediaUrl={}".format(
            urllib.parse.quote_plus(self._construct_image_url(image_file))
        )
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'X-DEVELOPER-KEY': os.environ.get("LOGOGRAB_KEY")
        }

        response = requests.request(
            "POST", self.BASE_URL, data=payload, headers=headers
        )
        import ipdb; ipdb.set_trace()
        return set(
            map(lambda x: x['name'], response.json()['data']['detections'])
        )

    def get_brands(self, image):
        raise NotImplementedError(
            "Waiting for permissions to send photo file to LogoGrab"
        )


image_file = "hibshman.net.jpeg"
brands = LogoDetection().get_brand_from_url(
    image_file=image_file
)


print(
    "Set (as in set theory) of brands detected from {}: {}".format(
        image_file, brands
    )
)

image_file = "nyuclubs.atspace.cc.jpeg"
brands = LogoDetection().get_brand_from_url(
    image_file=image_file
)

print(
    "Set (as in set theory) of brands detected from {}: {}".format(
        image_file, brands
    )
)
