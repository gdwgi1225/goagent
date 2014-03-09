#!/usr/bin/env python
# Flora_Pac by @leaskh
# www.leaskh.com, i@leaskh.com
# Based on chnroutes project (by Numb.Majority@gmail.com)

import re
import urllib2
import argparse
import math
import socket
import struct


def generate_pac(proxy):
    results  = fetch_ip_data()
    pacfile  = 'flora_pac.pac'
    rfile    = open(pacfile, 'w')
    results.insert(0, ('127.0.0.1',   '255.0.0.0',   0))
    results.insert(1, ('10.0.0.0',    '255.0.0.0',   0))
    results.insert(2, ('172.16.0.0',  '255.240.0.0', 0))
    results.insert(3, ('192.168.0.0', '255.255.0.0', 0))

    def ip(item):
        return item[0]

    results = sorted(results, key = ip)

    strLines = """// Flora_Pac by @leaskh
// www.leaskh.com, i@leaskh.com

function FindProxyForURL(url, host) {

    var list = ["""
    intLines = 0
    for ip,mask,_ in results:
        if intLines > 0:
            strLines = strLines + ','
        intLines = intLines + 1
        strLines = strLines + """
        [%s, %s]"""%(ip, mask)
    strLines = strLines + """
    ];

    function convertAddress(ipchars) {
        var bytes = ipchars.split('.');
        var result = ((bytes[0] & 0xff) << 24) |
                     ((bytes[1] & 0xff) << 16) |
                     ((bytes[2] & 0xff) <<  8) |
                      (bytes[3] & 0xff);
        return result;
    }

    function match(ip, list) {
        var left = 0, right = list.length;
        do {
            var mid = Math.floor((left + right) / 2),
                ip  = (ip & list[mid][1]) >>> 0,
                m   = (list[mid][0] & list[mid][1]) >>> 0;
            if (ip == m) {
                return true;
            } else if (ip > m) {
                left  = mid + 1;
            } else {
                right = mid;
            }
        } while (left + 1 <= right)
        return false;
    }

    if (isPlainHostName(host)
     || (host === '127.0.0.1')
     || (host === 'localhost')
     || (/\\b([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\\b/.test(host))) {
        return 'DIRECT';
    }

    var strIp = dnsResolve(host);
    if (!strIp) {
        return 'DIRECT';
    }

    var intIp = convertAddress(strIp);
    if (match(intIp, list)) {
        return 'DIRECT';
    }

    return '%s';

}
"""%(proxy)
    rfile.write(strLines)
    rfile.close()
    print ("Rules: %d items.\n"
           "Usage: Use the newly created %s as your web browser's automatic "
           "PAC(Proxy auto-config) file."%(intLines, pacfile))


def pac_server(port):
    if port <= 0:
        return
    import SimpleHTTPServer
    import SocketServer
    class DefaultHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/flora_pac.pac'
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    httpd = SocketServer.TCPServer(('0.0.0.0', port), DefaultHandler)
    print "PAC is now serving at: 0.0.0.0:%d"%(port)
    print "Check it out with: $ curl http://127.0.0.1:%d"%(port)
    httpd.serve_forever()


def fetch_ip_data():
    #fetch data from apnic
    print "Fetching data from apnic.net, it might take a few minutes, please wait..."
    url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
  # url=r'http://flora/delegated-apnic-latest' #debug
    data=urllib2.urlopen(url).read()

    cnregex=re.compile(r'apnic\|cn\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',re.IGNORECASE)
    cndata=cnregex.findall(data)

    results=[]
    prev_net=''

    for item in cndata:
        unit_items=item.split('|')
        starting_ip=unit_items[3]
        num_ip=int(unit_items[4])

        imask=0xffffffff^(num_ip-1)
        #convert to string
        imask=hex(imask)[2:]
        mask=[0]*4
        mask[0]=imask[0:2]
        mask[1]=imask[2:4]
        mask[2]=imask[4:6] #'0'
        mask[3]=imask[6:8] #'0'

        #convert str to int
        mask=[ int(i,16 ) for i in mask]
        mask="%d.%d.%d.%d"%tuple(mask)

        #mask in *nix format
        mask2=32-int(math.log(num_ip,2))
        results.append((starting_ip,mask,mask2))
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate proxy auto-config rules.")
    parser.add_argument('-x', '--proxy',
                        dest    = 'proxy',
                        default = 'PROXY 127.0.0.1:1998',
                        nargs   = '?',
                        help    = "Proxy Server, examples: "
                                  "SOCKS5 127.0.0.1:8964; "
                                  "SOCKS 127.0.0.1:8964; "
                                  "SOCKS5 127.0.0.1:8964; SOCKS 127.0.0.1:8964; DIRECT")
    parser.add_argument('-p', '--port',
                        dest    = 'port',
                        default = '0',
                        nargs   = '?',
                        help    = "Pac Server Port [OPTIONAL], examples: 8970")
    args = parser.parse_args()
    generate_pac(args.proxy)
    pac_server(int(args.port))
