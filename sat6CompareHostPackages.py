#!/usr/bin/env python

# File: sat6CompareHostPackages.py
# Author: Rich Jerrido <rjerrido@outsidaz.org>
# Purpose: given two hosts, show the package differences between them.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import getpass
import urllib2
import base64
import sys
import ssl
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--login", dest="login", help="Login user", metavar="LOGIN")
parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted",
                  metavar="PASSWORD")
parser.add_option("-s", "--server", dest="server", help="FQDN of sat6 instance", metavar="SERVER")
parser.add_option("--source-host", dest="sourcehost", help="Source Host for comparison", metavar="sourcehost")
parser.add_option("--target-host", dest="targethost", help="Target Host for comparison", metavar="targethost")
(options, args) = parser.parse_args()

if not (options.login and options.server and options.sourcehost and options.targethost):
    print "Must specify a login, server, sourcehost, and targethost (will prompt for password if omitted).  See usage:"
    parser.print_help()
    print "\nExample usage: ./sat6CompareHostPackages.py -l admin -s sat6.example.com --source-host foo.example.com --target-host bar.example.com"
    sys.exit(1)
else:
    login = options.login
    password = options.password
    server = options.server
    sourcehost = options.sourcehost
    targethost = options.targethost

if not password: password = getpass.getpass("%s's password:" % login)

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def get_host_package_list(host):
    url = "https://" + server + "/api/hosts/" + host
    try:
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (login, password)).strip()
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        hostiddata = json.load(result)
        hostid = hostiddata['id']

        myurl = "https://" + server + "/api/hosts/" + str(hostid) + "/packages?per_page=99999"
        request = urllib2.Request(myurl)
        base64string = base64.encodestring('%s:%s' % (login, password)).strip()
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request)
        hostdata = json.load(result)
        return hostdata['results']
    except urllib2.URLError, e:
        print "Error: cannot connect to the API: %s" % (e)
        print "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
        sys.exit(1)
    except Exception, e:
        print "FATAL Error - %s" % e
        sys.exit(2)



sourcehostPkg_list = []
for package in get_host_package_list(sourcehost):
    sourcehostPkg_list.append(package['nvra'])

targethostPkg_list = []
for package in get_host_package_list(targethost):
    targethostPkg_list.append(package['nvra'])

pkg_diff = list(set(sourcehostPkg_list) - set(targethostPkg_list))
print "There are %s packages that differ from %s -> %s"  % (len(pkg_diff), sourcehost, targethost)
for package in sorted(pkg_diff):
    print "\t%s" % package
print
pkg_diff = list(set(targethostPkg_list) - set(sourcehostPkg_list))
print "There are %s packages that differ from %s -> %s"  % (len(pkg_diff), targethost, sourcehost)
for package in sorted(pkg_diff):
    print "\t%s" % package

