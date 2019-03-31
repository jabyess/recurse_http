from http.server import HTTPServer, socketserver

HOSTNAME, PORT = "localhost", 4000


class Handler(socketserver.StreamRequestHandler):

    store = {}
    response = b'ok'

    def parse_kv(self, input):
        val = input.split('?')[1].split('=')
        if val[0] == 'key' and self.request_action == "GET":
            return val[1]
        else:
            return val

    def determine_action(self, input):
        valid = None
        if "?" in input and "=" in input:
            valid = True

        if valid:
            test = input[1:4]
            if test == 'set':
                return 'SET'
            elif test == 'get':
                return 'GET'

        return False

    def handle(self):
        req = self.rfile.readline().decode('ascii').strip()
        self.data = req.split(" ")
        self.request_action = self.determine_action(self.data[1])

        if self.request_action == "GET":
            key = self.parse_kv(self.data[1])
            if key in self.store:
                self.response = self.store[key].encode('ascii')
            else:
                self.response = f'no key {key} in store'.encode('ascii')

        elif self.request_action == "SET":
            vals = self.parse_kv(self.data[1])
            self.store[vals[0]] = vals[1]
            self.response = '200'.encode('ascii')
            print(self.store)

        self.wfile.write(self.response)
        self.finish()


if __name__ == '__main__':

    recurse_server = HTTPServer((HOSTNAME, PORT), Handler)

    print(f'starting server on {HOSTNAME}:{PORT}')

    recurse_server.serve_forever()

