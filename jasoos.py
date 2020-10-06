#!/usr/bin/python3
#Made by PR0_D3V1L
#06/04/2020

import json
import requests  # Install through  pip.
import re
import termcolor
import os 
import sys
import colorama
from termcolor import colored

colorama.init()

print(colored("""


     ____.                                 
    |    |____    __________   ____  ______
    |    \__  \  /  ___/  _ \ /  _ \/  ___/
/\__|    |/ __ \_\___ (  <_> |  <_> )___ \ 
\________(____  /____  >____/ \____/____  >
              \/     \/                 \/ 

                                                          
""", "red"))
print(colored("Coded By: PR0_D3V1L", "blue"))
print(colored("Version:  1.0", "blue"))
print(colored("Website:  http://vedpshukla.ml", "blue"))
print(colored("Description:This is one of the tools to find out the owner, internet provider and location of any website, domain or IP address. Checking IP addresses is useful for locating the origin of unwanted emails or the source of spam, virus and attacks- Try it out it’s free! ","blue"))
def is_valid_ip(ip):
    """Validates IP addresses.
    """
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)


def is_valid_ipv4(ip):
    """Validates IPv4 addresses.
    """
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None


def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros 
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None


# ---------------------------------------------------------------------------

# ->Inicio
api1_url_base = 'https://api.ip2country.info/ip?'
api2_url_base = 'https://api.db-ip.com/v2/free/'
api3_url_base = 'http://ip-api.com/json/'


def obtenerInformacionIP(ip: str, url: str):
    api_url = '{0}{1}'.format(url, ip)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


print("+--------------------------------------+")
ip = (input("Enter to IP >> ")).upper()
print("+--------------------------------------+")
if (not is_valid_ip(ip)):
    print("Insert to IPv4 or IPv6")
else:
    datoJSONAPI1 = obtenerInformacionIP(ip, api1_url_base)
    datoJSONAPI2 = obtenerInformacionIP(ip, api2_url_base)
    datoJSONAPI3 = obtenerInformacionIP(ip, api3_url_base)
    if (datoJSONAPI1 == None or datoJSONAPI2 == None or datoJSONAPI3 == None):
        print('Could not communicate with APIs')
    else:
        print("------------Scanning------------")
        print("\n")
        print("\n")
        print('AS => {0}'.format(datoJSONAPI3['as']))
        print('ISP => {0}'.format(datoJSONAPI3['isp']))
        print('Organization => {0}'.format(datoJSONAPI3['org']))
        print('Continent => {0} [{1}]'.format(datoJSONAPI2['continentName'], datoJSONAPI2['continentCode']))
        print('Country => {0} [{1}/{2}]'.format(datoJSONAPI1['countryName'], datoJSONAPI1['countryCode'], datoJSONAPI1['countryCode3']))
        print('Region => {0} [{1}]'.format(datoJSONAPI3['regionName'], datoJSONAPI3['region']))
        print('City => {0}'.format(datoJSONAPI3['city']))
        print('Postal Code => {0}'.format(datoJSONAPI3['zip']))
        print('Coordinates => {0},{1}'.format(datoJSONAPI3['lat'], datoJSONAPI3['lon']))
        print('Time zone => {0}'.format(datoJSONAPI3['timezone']))
        print('Emoji => {0}'.format(datoJSONAPI1['countryEmoji']))
print("\n")
print("----------Scanning Complete----------")
#Leave
