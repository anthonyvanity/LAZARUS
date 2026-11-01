#!/usr/bin/env python
# LAZARUS v0.1: Python 2.3-compatible, read-only LAN diagnostic agent.
# No shell commands from network, no installation, no cloud connection.
import BaseHTTPServer
import commands
import socket
import cgi

PORT = 8765

def collect():
    checks = [('OS', '/usr/bin/sw_vers'), ('Architecture', '/usr/bin/uname -m'), ('Disk', '/bin/df -h /')]
    output = []
    for label, cmd in checks:
        status, result = commands.getstatusoutput(cmd)
        output.append(label + '\n' + (result if status == 0 else 'Unavailable') + '\n')
    return '\n'.join(output)

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/diagnostics'):
            self.send_error(404)
            return
        report = collect()
        body = ('<html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>LAZARUS</title></head><body style="font-family:Helvetica,Arial;padding:18px">'
                '<h1>LAZARUS 0.1</h1><p>Legacy Mac diagnostics. Read only.</p>'
                '<p>Copy the report below into ChatGPT on your iPhone for analysis.</p>'
                '<textarea readonly rows="18" style="width:100%%">%s</textarea>'
                '<p>No upgrade or remote commands are enabled.</p></body></html>' % cgi.escape(report))
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = BaseHTTPServer.HTTPServer(('0.0.0.0', PORT), Handler)
    print 'LAZARUS diagnostic page listening on port %d' % PORT
    print 'Only use on a trusted private network. Press Control-C to stop.'
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print '\nLAZARUS stopped.'
        server.server_close()
