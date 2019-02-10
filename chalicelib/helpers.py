import ssl
import socket
import dns.resolver
import requests
import re


def get_ssl_information(domain):
    """Get details related with SSL
    :param domain: domain name.
    :type client: str

    :return: A dictionary with SSL details.
    :rtype: dictionary"""
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=domain)
    try:
        s.connect((domain, 443))
        cert = s.getpeercert()
        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
        return {'Issued to': issued_to, 'Valid from': cert['notBefore'], 'Valid till': cert['notAfter'],
                'Serial Number': cert['serialNumber']}
    except (ssl.SSLError, ssl.CertificateError):
        return {'Issued to': 'Error:SSL not found', 'Valid from': 'Error:SSL not found',
                'Valid till': 'Error:SSL not found', 'Serial Number': 'Error:SSL not found'}
    except socket.error:
        return {'Issued to': 'Host has failed to respond', 'Valid from': 'Host has failed to respond',
                'Valid till': 'Host has failed to respond', 'Serial Number': 'Host has failed to respond'}


def get_domain_nameServers(domain):
    """Get NameServers of domain.
    :param domain: Domain name.
    :type domain: str

    :return: Nameservers.
    :rtype: dict
    """
    domain = re.sub(r'(http(|s):\/\/|(www.|))', '', domain)

    ns_record = []
    try:
        for rdata in dns.resolver.query(domain, 'NS'):
            ns_record.append(str(rdata))
        return {'Nameservers': '|'.join(ns_record)}
    except Exception:
        return {'Nameservers': 'NameServers not found'}


def get_A_record(domain):
    """Get A record of domain.
    :param domain: Domain name.
    :type domain: str

    :return: A records.
    :rtype: dict
    """
    domain = re.sub(r'http(|s):\/\/', '', domain)

    try:
        a_record = []
        for rdata in dns.resolver.query(domain, 'A'):
            a_record.append(str(rdata.address))
        return {'A record': '|'.join(a_record)}
    except Exception:
        return {'A record': 'A record not found'}


def get_CNAME_record(domain):
    """Get CNAME record of domain.
    :param domain: Domain name.
    :type domain: str

    :return: CNAME records.
    :rtype: dict
    """
    domain = re.sub(r'http(|s):\/\/', '', domain)

    try:
        cname_record = []
        for rdata in dns.resolver.query(domain, 'CNAME'):
            cname_record.append(str(rdata.target))
        return {'CNAME record': '|'.join(cname_record)}
    except Exception:
        return {'CNAME record': 'CNAME record not found'}


def get_domain_type(domain):
    """Finds whether domain is primary,vanity or internal based on the redirect journey of the domain. 
    All expected exceptions are coverd such as DNS not resolved,SSL error,Too many redirects,etc.

    :param domain: Domain name.
    :type domain: str

    :return: dictionay with domain type or exception.
    :rtype: dict
    """
    domain = re.sub(r'http(|s):\/\/', '', domain)
    try:
        response = requests.get('http://' + domain.lower())
        domain = re.sub(r'http(|s):\/\/|(\/|\?)(.*)', '', domain)

        if (response.status_code == 404):
            return {'Domain type': '404 : Page not found'}
        elif ((domain != re.sub(r'http(|s):\/\/|(\/|\?)(.*)', '', response.url)) and
              (domain != re.sub(r'http(|s):\/\/www\.|(\/|\?)(.*)', '', response.url)) and
              (domain != re.sub(r'http(|s):\/\/|(\/|\?)(.*)', '', 'www.' + response.url))):
            return {'Domain type': 'Redirecting to ' + response.url}
        elif (response.status_code == 401):
            return {'Domain type': 'Domain under HTTP Authentication'}
        elif (response.status_code == 503):
            return {'Domain type': 'Maintenance mode'}
        elif (response.status_code == 200):
            return {'Domain type': 'Primary domain'}
        else:
            return {'Domain type': 'ERROR OCCURED'}

    except requests.exceptions.SSLError:
        return {'Domain type': 'SSL Error occured'}
    except requests.exceptions.ConnectionError:
        return {'Domain type': 'DNS not resolved'}
    except requests.exceptions.TooManyRedirects:
        return {'Domain type': 'Too many Redirections error'}
    except Exception:
        return {'Domain type': 'ERROR OCCURED'}
