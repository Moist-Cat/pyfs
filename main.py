import uuid
from http.server import SimpleHTTPRequestHandler, test
from hashlib import md5
import re

with open("template.html", "r+b") as file:
    template = file.read()


class DynamicFileHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/upload":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(template)
            return None
        super().do_GET()

    def do_POST(self):
        length = self.headers.get("content-length")
        if length:
            flen = int(length)

        offset = 0
        offset += len(self.rfile.readline())
        fname = self.rfile.readline().decode("utf8")
        offset += len(fname)
        # content-type 
        offset += len(self.rfile.readline())
        # muh final \n
        offset += len(self.rfile.readline())

        match = re.search('filename="[0-9\.a-z]+', fname)
        fname = fname[match.start() + 10 : match.end()]

        with open(fname, "w+b") as outfile:
            outfile.write(self.rfile.read(flen - offset))
        self.do_GET()


if __name__ == "__main__":
    test(HandlerClass=DynamicFileHandler)
