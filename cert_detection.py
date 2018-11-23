import ssl, socket
from urllib.parse import urlparse


class SSLCertificateNotFound(Exception):
    pass


def get_hostname(url):
    """
    parses hostname from a complete url or returns string back as is
    """
    parsed = urlparse(url)
    return parsed.netloc or url


def get_cert(hostname):
    """
    https://stackoverflow.com/questions/30862099/how-can-i-get-certificate-issuer-information-in-python
    """
    ctx = ssl.create_default_context()
    ss = ctx.wrap_socket(socket.socket(), server_hostname=hostname)

    try:
        ss.connect((hostname, 443))
    except ssl.SSLError as e:
        if e.reason == 'UNKNOWN_PROTOCOL':
            raise SSLCertificateNotFound(
                "Cannot find an SSL certificate at {}".format(hostname)
            )
        raise

    cert = ss.getpeercert()
    return cert


def get_cert_entities(url):
    try:
        cert = get_cert(get_hostname(url))
    except SSLCertificateNotFound:
        return {
            'issued_to': None,
            'issued_by': None,
        }

    subject = dict(x[0] for x in cert['subject'])
    issued_to = subject['commonName']
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['commonName']

    return {
        'issued_to': issued_to,
        'issued_by': issued_by,
    }
