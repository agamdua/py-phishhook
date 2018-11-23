import os
import requests


class ScreenShit:
    BASE_URL = "http://api.screenshotlayer.com/api/capture"

    def __init__(self, url):
        self.url = url
        self.access_key = os.environ.get('SCREENSHOT_ACCESS_KEY')

        if self.access_key is None:
            raise ValueError('access key not found in environmnent')

        # always be frugal in development
        # this ensures we don't make API calls if the file of the same name
        # is already present
        self.frugal_mode = os.environ.get('FRUGAL', True)

    @property
    def prepared_url(self):
        return "{}?access_key={}&url={}".format(
            self.BASE_URL,
            self.access_key,
            self.url,
        )

    def capture(self):
        """
        interfaces with https://screenshotlayer.com/documentation
        """
        response = requests.get(self.prepared_url)
        return response.content

    def save_as(self, fobj, fname):
        with open(fname, 'wb') as f:
            f.write(fobj)
        return fname

    def capture_and_save_as(self, fname):
        if self.frugal_mode:
            try:
                os.stat(fname)
                print(
                    "[FRUGAL MODE ON] "
                    "{} already downloaded, skipping capture".format(fname)
                )
                return fname
            except FileNotFoundError:
                print("cannot be frugal, you don't have the file you want")
                pass

        image = self.capture()
        return self.save_as(image, fname)

