#!/usr/bin/env python
"""Log in to a F5 Firepass SSL VPN from a command-line, without using F5's
browser-plugin and associated junk. Yay.

Works with OSX and linux, at the moment.

TODO: verify server certificate. (requires using pyopenssl instead of
socket.ssl)

Copyright 2006-2009, James Y Knight <foom@fuhm.net>

2009-12-24

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Disable deprecation warnings -- only I need to care.
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import socket, re, sys, os, time, fcntl, select, errno, signal
import getpass,getopt, types

try:
    import socks
except ImportError:
    socks = None

CONFIG_FILE = "~/.f5vpn-login.conf"

KEEPALIVE_TIMEOUT = 60 * 5

proxy_addr = None

def set_non_blocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def as_root(fn, *args, **kwargs):
    try:
        os.seteuid(0)
        return fn(*args, **kwargs)
    finally:
        os.seteuid(os.getuid())

def sts_result(sts):
    if os.WIFSIGNALED(sts):
        return -os.WTERMSIG(sts)
    elif os.WIFEXITED(sts):
        return os.WEXITSTATUS(sts)
    else:
        raise os.error, "Not signaled or exited???"

def run_as_root(args, stdin=None):
    if stdin is not None:
        pipe_r, pipe_w = os.pipe()
    else:
        pipe_r, pipe_w = None, None

    pid = os.fork()
    if pid == 0:
        if pipe_r is not None:
            # setup stdin pipe
            os.dup2(pipe_r, 0)
            os.close(pipe_r)
            os.close(pipe_w)

        os.seteuid(0)
        os.setuid(0)
        try:
            os.execv(args[0], args)
        except:
            os._exit(127)
    else:
        if pipe_r is not None:
            os.close(pipe_r)
            os.write(pipe_w, stdin)
            os.close(pipe_w)
        wpid, sts = os.waitpid(pid, 0)
        code = sts_result(sts)
        if code != 0:
            raise Exception("%r: exited with result %d"% (args, code))


class Platform:
    def setup_route(self, ifname, gateway_ip, net, bits, action):
        pass

    def setup_dns(self, iface_name, service_id, dns_servers, dns_domains, revdns_domains, override_gateway):
        pass

    def teardown_dns(self):
        pass

class DummyPlatform:
    def setup_route(self, ifname, gateway_ip, net, bits, action):
        print "setup_route(ifname=%r, gateway_ip=%r, net=%r, bits=%r, action=%r" % (ifname, gateway_ip, net, bits, action)

    def setup_host_route(self, ifname, gateway_ip, net, bits):
        print "teardown_route(ifname=%r, gateway_ip=%r, net=%r, bits=%r" % (ifname, gateway_ip, net, bits)

    def setup_dns(self, iface_name, service_id, dns_servers, dns_domains, revdns_domains, override_gateway):
        print "setup_dns(iface_name=%r, service_id=%r, dns_servers=%r, dns_domains=%r, revdns_domains=%r, override_gateway=%r)" % (iface_name, service_id, dns_servers, dns_domains, revdns_domains, override_gateway)

    def teardown_dns(self):
        print "teardown_dns()"

class DarwinPlatform(Platform):
    def __init__(self):
        if os.path.exists("/sbin/route"):
            self.route_path="/sbin/route"
        elif os.path.exists("/usr/bin/route"):
            self.route_path="/usr/bin/route"
        else:
            raise Exception("Couldn't find route command")

    def setup_route(self, ifname, gateway_ip, net, bits, action):
        args = [self.route_path, action, '-net', "%s/%s" % (net, bits)]
        if ifname:
            args += ['-interface', ifname]
        else:
            args += [gateway_ip]
        run_as_root(args)

    def load_SystemConfigurationFramework(self):
        try:
            # If it's already been wrapped, we're done.
            import SystemConfiguration
            return SystemConfiguration
        except ImportError:
            # Nope, so, try again, the hard way...
            import objc
            SystemConfiguration=types.ModuleType('SystemConfiguration')
            SCbndl = objc.loadBundle(SystemConfiguration.__name__, SystemConfiguration.__dict__,
                                     bundle_identifier="com.apple.SystemConfiguration")

            objc.loadBundleFunctions(SCbndl, SystemConfiguration.__dict__, [
                    (u'SCDynamicStoreCreate', '@@@@@'),
                    (u'SCDynamicStoreSetValue', 'B@@@')
                    ])
            return SystemConfiguration

    def setup_dns(self, iface_name, service_id, dns_servers, dns_domains, revdns_domains, override_gateway):
        """Setup DNS the OSX magic way."""
        # Preferentially use the SystemConfiguration library (included with OSX
        # 10.5) if available, as scutil has a command-length limitation of 256
        # chars. With 256 chars it's generally not reasonable to add in the
        # revdns domains, so don't bother trying.

        # NOTE: There's a 3rd party SystemConfiguration package for 10.4 which
        # seems to have a different API (that I don't support currently)
        try:
            SystemConfiguration=self.load_SystemConfigurationFramework()
            SystemConfiguration.SCDynamicStoreCreate
        except:
            # fall back to scutil.
            config = "d.init\n"
            config += "d.add ServerAddresses * %s\n" % ' '.join(dns_servers)
            if override_gateway:
                config += "d.add SearchDomains * %s\n" % ' '.join(dns_domains)
            else:
                config += "d.add SupplementalMatchDomains * %s\n" % ' '.join(dns_domains)
            config += "set State:/Network/Service/%s/DNS\n" % service_id

            run_as_root(['/usr/sbin/scutil'], stdin=config)
        else:
            def setup_helper():
                sc = SystemConfiguration.SCDynamicStoreCreate(None, "f5vpn-login", None, None)
                d = SystemConfiguration.NSMutableDictionary.new()
                d[u'ServerAddresses'] = dns_servers
                if override_gateway:
                    d[u'SearchDomains'] = dns_domains
                else:
                    d[u'SupplementalMatchDomains'] = dns_domains + revdns_domains
                SystemConfiguration.SCDynamicStoreSetValue(sc, 'State:/Network/Service/%s/DNS' % service_id, d)
            as_root(setup_helper)


class Linux2Platform(Platform):
    def setup_route(self, ifname, gateway_ip, net, bits, action):
        if bits == 32:
            host_or_net = "-host"
        else:
            host_or_net = "-net"
        run_as_root(['/sbin/route', action, host_or_net,
                     "%s/%s" % (net, bits),
                     'gw', gateway_ip])

class FreeBSD6Base(Platform):
    def setup_route(self, ifname, gateway_ip, net, bits, action):
        args = ['/sbin/route', action, "%s/%s" % (net, bits)]
        if ifname:
            args += ['-interface', ifname]
        else:
            args += [gateway_ip]
        run_as_root(args)

class ManualFrobbingDNSMixin:
    resolv_conf_timestamp = 0

    def setup_dns(self, iface_name, service_id, dns_servers, dns_domains, revdns_domains, override_gateway):
        if override_gateway:
            old_resolv_conf = []
        else:
            old_resolv_conf = open("/etc/resolv.conf").readlines()

        other_lines = []
        search = ''
        nses = []
        for line in old_resolv_conf:
            line = line.rstrip('\n')
            if line.startswith('search ') or line.startswith('domain '):
                # domain entry is simply an alternative spelling for search
                search = line.split(' ', 1)[1]
            elif line.startswith('nameserver '):
                nses.append(line.split(' ', 1)[1])
            else:
                other_lines.append(line)

        new_resolv_conf = []
        new_resolv_conf.append("search %s %s" % (' '.join(dns_domains), search))
        for ns in dns_servers + nses:
            new_resolv_conf.append("nameserver %s" % ns)
        new_resolv_conf.extend(other_lines)
        new_resolv_conf.append('')

        def _create_file():
            os.rename('/etc/resolv.conf', '/etc/resolv.conf.f5_bak')
            open('/etc/resolv.conf', 'w').write('\n'.join(new_resolv_conf))
        as_root(_create_file)

        self.resolv_conf_timestamp = os.stat('/etc/resolv.conf').st_mtime

    def teardown_dns(self):
        as_root(self._teardown_dns)

    def _teardown_dns(self):
        try:
            if self.resolv_conf_timestamp == 0:
                pass
            elif os.stat('/etc/resolv.conf').st_mtime == self.resolv_conf_timestamp:
                os.rename('/etc/resolv.conf.f5_bak', '/etc/resolv.conf')
            else:
                sys.stderr.write("Not restoring resolv.conf: modified by another process.\n")
                os.unlink('/etc/resolv.conf.f5_bak')
        except:
            pass

class ResolvConfHelperDNSMixin:
    def setup_dns(self, iface_name, service_id, dns_servers, dns_domains, revdns_domains, override_gateway):
        # FIXME: should I be doing something different here based on override_gateway?

        # ResolvConf is a system for managing your resolv.conf file in a
        # structured way on unix systems. When it is installed, go through it,
        # rather than munging the file manually (and thus causing potential
        # conflicts)

        # We append tun- to the interface so the proper record order is
        # established with the resolvconf distribution.  Since we're essentially
        # using ppp for the same reason as most people would use tun, this
        # should be okay
        self.iface_name = iface_name
        cmd = "nameserver %s\nsearch %s\n" % (' '.join(dns_servers), ' '.join(dns_domains))
        run_as_root(['/sbin/resolvconf', '-a', 'tun-%s' % iface_name], stdin=cmd)

    def teardown_dns(self):
        as_root(self._teardown_dns)

    def _teardown_dns(self):
        try:
            run_as_root(["/sbin/resolvconf", '-d', 'tun-%s' % self.iface_name])
        except:
            pass

class Linux2ManualPlatform(ManualFrobbingDNSMixin, Linux2Platform):
    pass

class Linux2ResolvconfPlatform(ResolvConfHelperDNSMixin, Linux2Platform):
    pass

class FreeBSD6Platform(ManualFrobbingDNSMixin, FreeBSD6Base):
    pass

def get_platform():
    if sys.platform == "darwin":
        return DarwinPlatform()
    elif sys.platform == "linux2":
        # Choose a dns resolver setup routine
        if os.path.exists('/sbin/resolvconf'):
            return Linux2ResolvconfPlatform()
        else:
            return Linux2ManualPlatform()
    elif sys.platform == "freebsd6":
        return FreeBSD6Platform()
    elif sys.platform == "freebsd7":
        return FreeBSD6Platform()
    elif sys.platform == "freebsd8":
        return FreeBSD6Platform()
    else:
        # Other Unix-like platforms aren't supported at the moment...but there's
        # no reason they can't be, when someone with such a platform tells me
        # the syntax for their "route" command. Patches welcome!
        raise Exception("Don't know how to setup routes/dns for platform %r" % sys.platform)
platform = get_platform()

def readline_from_sock(s):
    output = ''
    while 1:
        data = s.recv(1)
        if not data:
            break
        elif data == '\n':
            break
        elif data != '\r':
            output += data
    return output

def proxy_connect(ip, port):
    # Connect a socket to ip and port, and return a socket object.
    # If a proxy is defined, connect via the proxy.
    if proxy_addr and proxy_addr[0] == 'http':
        s = socket.socket()
        s.connect(proxy_addr[1:])
        s.send("CONNECT %s:%d HTTP/1.0\r\n\r\n" % (ip, port))
        statusline = readline_from_sock(s).split(' ')
        if len(statusline) < 2 or statusline[1] != '200':
            raise Exception("Proxy returned bad status for CONNECT: %r" % ' '.join(statusline))
        while 1: # Read remaining headers, if any
            line = readline_from_sock(s)
            if line == '':
                break
        # Now the ssl connection is going
    elif proxy_addr and proxy_addr[0] == 'socks5':
        # Socks method
        s = socks.socksocket()
        s.setproxy(socks.PROXY_TYPE_SOCKS5, proxy_addr[1], proxy_addr[2])
        s.connect((ip,port))
    else:
        s = socket.socket()
        s.connect((ip,port))
    return s

def parse_hostport(host, default_port=0):
    ipport=host.split(':')
    if len(ipport) == 1:
        ip = ipport[0]
        port = 443
    else:
        ip = ipport[0]
        port = int(ipport[1])
    return ip, port

def send_request(host, request):
    ip, port = parse_hostport(host, 443)
    s = proxy_connect(ip, port)
    ssl = socket.ssl(s)
    ssl.write(request)
    data = ''
    while 1:
        try:
            data += ssl.read()
        except (socket.error, socket.sslerror):
            break
    #print data
    return data

def get_vpn_client_data(host):
    # Some FirePass servers are configured to redirect to an external "pre-login
    # check" server.  This server is supposed to run some random additional
    # checks to see if it likes you, and then redirects back to the firepass,
    # with the client_data gunk as an extra POST variable.

    # If such an element is present, the firepass will refuse login unless we
    # pass it through to the my.activation.php3 script. So, do so. Secureetay!

    request = """GET /my.logon.php3?check=1&no_inspectors=1 HTTP/1.0\r
Accept: */*\r
Accept-Language: en\r
Cookie: uRoamTestCookie=TEST; VHOST=standard\r
Referer: https://%(host)s/my.activation.php3\r
User-Agent: Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.9.2\r
Host: %(host)s\r
\r
""" % dict(host=host)
    result = send_request(host, request)
    match = re.search('document.external_data_post_cls.client_data.value = \"([\w=]+)\"', result)
    if match:
        return match.group(1)

    match = re.search('name="client_data" value="([\w=]+)"', result)
    if match:
        return match.group(1)
    return ''

def do_login(host, username, password):
    client_data = get_vpn_client_data(host)

    body="rsa_port=&vhost=standard&username=%(user)s&password=%(password)s&client_data=%(client_data)s&login=Logon&state=&mrhlogonform=1&miniui=1&tzoffsetmin=1&sessContentType=HTML&overpass=&lang=en&charset=iso-8859-1&uilang=en&uicharset=iso-8859-1&uilangchar=en.iso-8859-1&langswitcher=" % dict(user=username, password=password, client_data=client_data)

    request = """POST /my.activation.php3 HTTP/1.0\r
Accept: */*\r
Accept-Language: en\r
Cookie: VHOST=standard; uRoamTestCookie=TEST\r
Content-Type: application/x-www-form-urlencoded\r
Referer: https://%(host)s/my.activation.php3\r
User-Agent: Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.9.2\r
Host: %(host)s\r
Content-Length: %(len)d\r
\r
%(body)s
""" % dict(host=host, len=len(body), body=body)

    result = send_request(host, request)

    session = None
    pat = re.compile('^Set-Cookie: MRHSession=([^;]*);', re.MULTILINE)
    for match in pat.finditer(result):
        sessid = match.group(1)
        if sessid == "deleted":
            session = None
        else:
            session = sessid

    if session is None:
        if "Either Username or Password do not match!" in result:
            sys.stderr.write("Wrong user or password, sorry.\n")
            sys.exit(3)
            return None

        match = re.search("(Challenge: [^<]*)", result)
        if match:
            sys.stderr.write(match.group(1)+"\n")
            return None

        sys.stderr.write("Login process failed, unknown output. Sorry!\n")
        sys.stderr.write(result)
        sys.stderr.write("\n")
        sys.exit(1)
    else:
        return session

def get_vpn_menu_number(host, session):
    # Find out the "Z" parameter to use to open a VPN connection
    request = """GET /vdesk/vpn/index.php3?outform=xml HTTP/1.0\r
Accept: */*\r
Accept-Language: en\r
Cookie: uRoamTestCookie=TEST; VHOST=standard; MRHSession=%(session)s\r
Referer: https://%(host)s/my.activation.php3\r
User-Agent: Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.9.2\r
Host: %(host)s\r
\r
""" % dict(host=host, session=session)
    result = send_request(host, request)
    match = re.search('<favorite id="Z=([^"]*)">', result)
    if match:
        menu_number = match.group(1)
        result = send_request(host, request)
        return match.group(1)
    else:
        if re.search('^Location: /my.logon.php3', result):
            # a redirect to the login page.
            sys.stderr.write("Old session no longer valid.\n")
        return None

def get_VPN_params(host, session, menu_number):
    request = """GET /vdesk/vpn/connect.php3?Z=%(menu_number)s HTTP/1.0\r
Accept: */*\r
Accept-Language: en\r
Cookie: uRoamTestCookie=TEST; VHOST=standard; MRHSession=%(session)s\r
Referer: https://%(host)s/vdesk/index.php3\r
User-Agent: Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.9.2\r
Host: %(host)s\r
\r
""" % dict(menu_number=menu_number, session=session, host=host)
    result = send_request(host, request)
    #print "RESULT:", result

    # Try to find the plugin parameters
    matches = list(re.finditer("<embed [^>]*?(version=[^>]*)>", result))
    if not matches:
        # A new version of the server has switched to using javascript to write
        # the parameters, now, so try matching that too.
        matches = list(re.finditer("document.writeln\('(version=[^)]*)'\)", result))

    if not matches:
        if re.search('^Location: /my.logon.php3', result):
            # a redirect to the login page.
            sys.stderr.write("Old session no longer valid.\n")
            return None
        sys.stderr.write("Embed info output:\n")
        sys.stderr.write(result)
        return None

    match = matches[-1]
    params = match.group(1)
    params = params.replace(' ', '&').replace('"', '')
    paramsDict = decode_params(params)
    #print paramsDict
    return paramsDict


def decode_params(paramsStr):
    paramsDict = {}
    for param in paramsStr.split('&'):
        k,v = param.split('=', 1)
        if re.match('q[0-9]+', k):
            k,v = v.decode('hex').split('=', 1)
        paramsDict[k] = v

    return paramsDict

class LogWatcher:
    """Collect (iface_name, tty, local_ip, remote_ip) from the ppp log messages
    and call ppp_ip_up when they've all arrived."""

    collected_log = ''
    iface_name = tty = remote_ip = local_ip = None
    notified = False

    def __init__(self, ip_up):
        self.ip_up = ip_up

    def _get_match(self, exp):
        match = re.search(exp, self.collected_log, re.MULTILINE)
        if match is not None:
            return match.group(1)

    def process(self, logmsg):
        print "PPPD LOG: %r" % logmsg

        self.collected_log += logmsg

        if self.iface_name is None:
            self.iface_name = self._get_match("Using interface (.*)$")
        if self.tty is None:
            self.tty = self._get_match("Connect: .* <--> (.*)$")
        if self.remote_ip is None:
            self.remote_ip = self._get_match("remote IP address (.*)$")
        if self.local_ip is None:
            self.local_ip = self._get_match("local  IP address (.*)$")

        if not (self.notified or
                self.iface_name is None or self.tty is None or
                self.remote_ip is None or self.local_ip is None):
            print "CALLING ip_up%r" % ((self.iface_name, self.tty, self.local_ip, self.remote_ip),)
            self.notified = True
            self.ip_up(self.iface_name, self.tty, self.local_ip, self.remote_ip)

keepalive_socket = None
def set_keepalive_host(host):
    global keepalive_socket
    keepalive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    keepalive_socket.connect((host, 7))
    keepalive_socket.setblocking(0)

def run_event_loop(pppd_fd, ssl_socket, ssl, logpipe_r, ppp_ip_up):
    ssl_socket.setblocking(0)
    set_non_blocking(pppd_fd)
    set_non_blocking(logpipe_r)

    # Tiny little event-loop: don't try this at home.
    ssl_write_blocked_on_read = False
    ssl_read_blocked_on_write = False
    data_to_pppd = ''
    data_to_ssl = ''
    data_to_ssl_buf2 = ''

    def sigusr1(sig, frame):
        sys.stderr.write("ssl_write_blocked_on_read=%r, ssl_read_blocked_on_write=%r, data_to_pppd=%r, data_to_ssl=%r, data_to_ssl_buf2=%r, time_since_last_activity=%r\n" % (ssl_write_blocked_on_read, ssl_read_blocked_on_write, data_to_pppd, data_to_ssl, data_to_ssl_buf2, time.time() - last_activity_time))
    signal.signal(signal.SIGUSR1, sigusr1)

    logwatcher = LogWatcher(ppp_ip_up)

    last_activity_time = time.time()

    while 1:
        reads = [logpipe_r]
        writes = []
        # try to write data to pppd if pending, otherwise read more data from ssl
        if data_to_pppd:
            writes.append(pppd_fd)
        else:
            if ssl_read_blocked_on_write:
                writes.append(ssl_socket)
            else:
                reads.append(ssl_socket)

        # Conversely, write data to ssl if pending, otherwise read more data from pppd
        if data_to_ssl:
            if ssl_write_blocked_on_read:
                reads.append(ssl_socket)
            else:
                writes.append(ssl_socket)
        else:
            reads.append(pppd_fd)

        if keepalive_socket:
            timeout = max(last_activity_time + KEEPALIVE_TIMEOUT - time.time(), 0)
        else:
            timeout = None

        # Run the select, woot
        try:
            reads,writes,exc = select.select(reads, writes, [], timeout)
        except select.error, se:
            if se.args[0] not in (errno.EAGAIN, errno.EINTR):
                raise
            continue # loop back around to try again

        if keepalive_socket and not reads and not writes:
            # Returned from select because of timeout (probably)
            if time.time() - last_activity_time > KEEPALIVE_TIMEOUT:
                sys.stderr.write("Sending keepalive\n")
                keepalive_socket.send('keepalive')


        #print "SELECT GOT:", reads,writes,exc

        # To simplify matters, don't bother with what select returned. Just try
        # everything; it doesn't matter if it fails.

        # Read data from log pipe
        try:
            logmsg = os.read(logpipe_r, 10000)
            if not logmsg: #EOF
                print "EOF on logpipe_r"
                break
            logwatcher.process(logmsg)
        except OSError, se:
            if se.args[0] not in (errno.EAGAIN, errno.EINTR):
                raise

        # Read data from pppd
        if not data_to_ssl:
            try:
                data_to_ssl = os.read(pppd_fd, 10000)
                if not data_to_ssl: #EOF
                    print "EOF on pppd"
                    break
                #print "READ PPPD: %r" % data_to_ssl
            except OSError, se:
                if se.args[0] not in (errno.EAGAIN, errno.EINTR):
                    raise

        # Read data from SSL
        if not data_to_pppd:
            try:
                ssl_read_blocked_on_write = False
                data_to_pppd = ssl.read()
                if not data_to_pppd: #EOF
                    print "EOF on ssl"
                    break
                last_activity_time = time.time()
            except socket.sslerror, se:
                if se.args[0] == socket.SSL_ERROR_WANT_READ:
                    pass
                elif se.args[0] == socket.SSL_ERROR_WANT_WRITE:
                    ssl_read_blocked_on_write = True
                else:
                    raise
            #print "READ SSL: %r" % data_to_pppd

        # Write data to pppd
        if data_to_pppd:
            try:
                num_written = os.write(pppd_fd, data_to_pppd)
                #print "WROTE PPPD: %r" % data_to_pppd[:num_written]
                data_to_pppd = data_to_pppd[num_written:]
            except OSError, se:
                if se.args[0] not in (errno.EAGAIN, errno.EINTR):
                    raise

        # Write data to SSL
        if not data_to_ssl_buf2 and data_to_ssl:
            # Write in SSL is not like unix write; you *must* call it with the
            # same pointer as previously if it fails.  Otherwise, it'll raise a
            # "bad write retry" error.
            data_to_ssl_buf2 = data_to_ssl
            data_to_ssl = ''

        if data_to_ssl_buf2:
            try:
                ssl_write_blocked_on_read = False
                num_written = ssl.write(data_to_ssl_buf2)
                # should always either write all data, or raise a WANT_*
                assert num_written == len(data_to_ssl_buf2)
                data_to_ssl_buf2 = ''
                last_activity_time = time.time()
            except socket.sslerror, se:
                if se.args[0] == socket.SSL_ERROR_WANT_READ:
                    ssl_write_blocked_on_read = True
                elif se.args[0] == socket.SSL_ERROR_WANT_WRITE:
                    pass
                else:
                    raise
            #print "WROTE SSL: %r" % data_to_ssl[:num_written]

def shutdown_pppd(pid):
    res_pid, result = os.waitpid(pid, os.WNOHANG)
    if res_pid and result != 0:
        sys.stdout.write("PPPd exited unexpectedly with result %s\n" % result)
    else:
        sys.stdout.write("Shutting down pppd, please wait...\n")
        os.kill(pid, signal.SIGTERM)
        os.waitpid(pid, 0)

mask2bits = {}
for x in range(33):
    mask2bits[2**32 - 2**(32-x)] = x

def parts_to_int(s):
    num = 0
    for n in parts:
        num = num * 256 + n
    num *= 256 ** (4 - len(parts))
    return num

def parse_net_bits(routespec):
    # This routine parses the following formats:
    # w.x.y.z/numbits
    # w.x.y.z/A.B.C.D
    # w[.x[.y[.z]]] (netmask implicit in number of .s)
    if '/' in routespec:
        net, bits = routespec.split('/', 1)
        netparts = map(int, net.split('.'))
        while len(netparts) < 4:
            netparts.append(0)

        if '.' in bits:
            parts = map(int, bits.split('.'))
            netmaskparts = map(int, bits.split('.'))
            netmask = 0
            for n in netmaskparts:
                netmask = netmask * 256 + n
            netmask *= 256 ** (4 - len(netmaskparts))

            bits = mask2bits.get(netmask)
            if bits is None:
                raise Exception("Non-contiguous netmask in routespec: %s\n" % (routespec,))
        else:
            bits = int(bits)
    else:
        netparts = map(int, routespec.split('.'))
        bits = len(netparts) * 8
        while len(netparts) < 4:
            netparts.append(0)

    return netparts, bits

def routespec_to_revdns(netparts, bits):
    domain = 'in-addr.arpa'
    i = 0
    while bits >= 8:
        domain = str(netparts[i]) + '.' + domain
        bits -= 8
        i += 1

    if bits == 0:
        return [domain]
    else:
        remaining_bits = 8 - bits
        start_addr = netparts[i] & ~(2**remaining_bits - 1)
        return [(str(n) + '.' + domain)
                for n in range(start_addr, start_addr + 2**(remaining_bits))]

def execPPPd(params):
    tunnel_host=params['tunnel_host0']
    tunnel_port=int(params['tunnel_port0'])

    serviceid = "f5vpn-%s"%tunnel_host

    request = """GET /myvpn?sess=%s HTTP/1.0\r
Cookie: MRHSession=%s\r
\r
""" % (params['Session_ID'], params['Session_ID'])

    for i in range(5):
        try:
            ssl_socket = proxy_connect(tunnel_host, tunnel_port)
            ssl_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            ssl = socket.ssl(ssl_socket)
            ssl.write(request)
            initial_data = ssl.read()
            break
        except socket.sslerror, e:
            # Sometimes the server seems to respond with "EOF occurred in violation of protocol"
            # instead of establishing the connection. Try to deal with this by retrying...
            if e.args[0] != 8:
                raise
            sys.stderr.write("VPN socket unexpectedly closed during connection setup, retrying (%d/5)...\n" % (i + 1))

    # Make new PTY
    (pppd_fd, slave_pppd_fd) = os.openpty()

    # Make log pipe
    logpipe_r,logpipe_w = os.pipe()

    # If the server says to redirect the default gateway, we need to first add
    # an explicit route for the VPN server with the /current/ default gateway.
    # The default gw will automatically be set by pppd.
    override_gateway = ('UseDefaultGateway0' in params)
    if override_gateway:
        tunnel_ip = ssl_socket.getpeername()[0]
        # FIXME: This is a total hack...and incorrect in some cases, too.  But
        # it'll work in the normal case where the VPN server isn't on your local
        # subnet.  This should really be using some (platform-specific) method
        # of finding the current route to tunnel_ip instead of assuming that's
        # the default route.
        gw_ip = os.popen("netstat -rn|grep '^default\|^0.0.0.0'|awk '{print $2}'").read().split()[0]
        sys.stderr.write("Detected current default route: %r\n" % gw_ip)
        sys.stderr.write("Attempting to delete and override route to VPN server.\n")
        try:
            platform.setup_route('', gw_ip, tunnel_ip, 32, 'delete')
        except:
            pass
        platform.setup_route('', gw_ip, tunnel_ip, 32, 'add')

    pid = os.fork()
    if pid == 0:
        os.close(ssl_socket.fileno())
        # Setup new controlling TTY
        os.close(pppd_fd)
        os.setsid()
        os.dup2(slave_pppd_fd, 0)
        os.close(slave_pppd_fd)

        # setup log pipe
        os.dup2(logpipe_w, 4)
        os.close(logpipe_r)
        os.close(logpipe_w)

        # Become root
        os.seteuid(0)
        os.setuid(0)

        # Run pppd
        args = ['pppd', 'logfd', '4', 'noauth', 'nodetach',
                'crtscts', 'passive', 'ipcp-accept-local', 'ipcp-accept-remote',
                'local', 'nodeflate', 'novj', ]

        if override_gateway:
            args.append('defaultroute')
        else:
            args.append('nodefaultroute')

        if sys.platform == "darwin":
            args.extend(['serviceid', serviceid])

        try:
            os.execvp("pppd", args)
        except:
            os._exit(127)

    os.close(slave_pppd_fd)
    os.close(logpipe_w)
    def ppp_ip_up(iface_name, tty, local_ip, remote_ip):
        revdns_domains = []
        if params.get('LAN0'):
            for routespec in params['LAN0'].split(' '):
                net, bits = parse_net_bits(routespec)
                platform.setup_route(iface_name, local_ip, '.'.join(map(str, net)), bits, 'add')
                revdns_domains.extend(routespec_to_revdns(net, bits))

        # sending a packet to the "local" ip appears to actually send data
        # across the connection, which is the desired behavior.
        set_keepalive_host(local_ip)

        if params.get('DNS0'):
            platform.setup_dns(iface_name, serviceid,
                               params['DNS0'].split(','),
                               params['DNSSuffix0'].split(' '), revdns_domains, override_gateway)
        print "VPN link is up!"

    try:
        run_event_loop(pppd_fd, ssl_socket, ssl, logpipe_r, ppp_ip_up)
    finally:
        if params.get('DNS0'):
            platform.teardown_dns()
        as_root(shutdown_pppd, pid)
        if override_gateway:
            try:
                platform.setup_route('', gw_ip, tunnel_ip, 32, 'delete')
            except:
                pass

def usage(exename, s):
    print >>s, "Usage: %s [--{http,socks5}-proxy=host:port] [[user@]host]" % exename

def get_prefs():
    try:
        conf = open(os.path.expanduser(CONFIG_FILE))
    except:
        return None

    return conf.readline()

def write_prefs(line):
    try:
        f = open(os.path.expanduser(CONFIG_FILE), 'w')
        f.write(line)
    except:
        print "Couldn't write prefs file: %s" % CONFIG_FILE

# 2.3.5 or higher is required because of this (2.2.X ought to work too, but I've not tested it):
#     ------------------------------------------------------------------------
#     r37117 | doko | 2004-08-24 17:48:15 -0400 (Tue, 24 Aug 2004) | 4 lines
#     [Patch #945642] Fix non-blocking SSL sockets, which blocked on reads/writes in Python 2.3.
#      Taken from HEAD, tested as part of the unstable and testing Debian packages since May on
#      various architectures.

def main(argv):
    global proxy_addr
    if '--help' in argv:
        usage(argv[0], sys.stdout)
        sys.exit(0)

    if sys.version_info < (2,3,5):
        sys.stderr.write("Python 2.3.5 or later is required.\n")
        sys.exit(1)

    if os.geteuid() != 0:
        sys.stderr.write("ERROR: \n")
        sys.stderr.write(
"  This script must be run as root. Preferably setuid (via companion .c\n"
"  program), but it'll work when invoked as root directly, too.\n")
        sys.exit(1)

    # Set effective uid to userid; will become root as necessary
    os.seteuid(os.getuid())
    user = getpass.getuser()

    try:
        opts,args=getopt.getopt(argv[1:], "", ['http-proxy=', 'socks5-proxy='])
    except getopt.GetoptError, e:
        sys.stderr.write("Unknown option: %s\n" % e.opt)
        usage(argv[0], sys.stderr)
        sys.exit(1)

    if len(args) > 1:
        usage(argv[0], sys.stderr)
        sys.exit(1)

    prefs = get_prefs()
    old_session = None
    userhost = None
    if prefs is not None:
        path, userhost, old_session = prefs.split('\0')

    if len(args) > 0:
        if args[0] != userhost:
            # Don't attempt to reuse session if switching users or servers.
            old_session = None
        userhost = args[0]

    if userhost is None:
        sys.stderr.write("The host argument must be provided the first time.\n")
        sys.exit(1)

    if '@' in userhost:
        user,host = userhost.rsplit('@', 1)
    else:
        host = userhost

    for opt,val in opts:
        if opt in ('--http-proxy'):
            proxy_addr = ('http',) + parse_hostport(val)
            sys.stderr.write("Using proxy: %r\n" % (proxy_addr,))
        elif opt in ('--socks5-proxy'):
            if socks is None:
                sys.stderr.write("Cannot use a socks5 proxy: you do not seem to have the socks module available.\n")
                sys.stderr.write("Please install SocksiPy: http://socksipy.sourceforge.net/\n")
                sys.exit(1)
            proxy_addr = ('socks5',) + parse_hostport(val)
            sys.stderr.write("Using proxy: %r\n" % (proxy_addr,))

    params = None

    if old_session:
        print "Trying old session..."
        menu_number = get_vpn_menu_number(host, old_session)
        if menu_number is not None:
            params = get_VPN_params(host, old_session, menu_number)
            session = old_session

    if params is None:
        while True:
            password = getpass.getpass("password for %s@%s? " % (user, host))
            session = do_login(host, user, password)
            if session is not None:
                print "Session id gotten:", session
                break

        print "Getting params..."
        menu_number = get_vpn_menu_number(host, session)
        if menu_number is None:
            sys.stderr.write("Unable to find the 'Network Access' entry in main menu. Do you have VPN access?\n")
            sys.exit(1)

        params = get_VPN_params(host, session, menu_number)

    if params is None:
        print "Couldn't get embed info. Sorry."
        sys.exit(2)

    write_prefs('\0'.join(['', userhost, session]))
    print "Got plugin params, execing vpn client"

    try:
        execPPPd(params)
    except KeyboardInterrupt:
        pass
    except SystemExit, se:
        print se
    print "Shut-down."

if __name__ == '__main__':
    main(sys.argv)