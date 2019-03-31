from http.server import HTTPServer, socketserver

HOSTNAME, PORT = "localhost", 4000


class Handler(socketserver.BaseRequestHandler):

    store = {}
    
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
        self.data = str(self.request.recv(1024).strip()).split(" ")
        self.request_action = self.determine_action(self.data[1])

        if self.request_action == "GET":
            key = self.parse_kv(self.data[1])
            self.response = self.store[key]

        elif self.request_action == "SET":
            vals = self.parse_kv(self.data[1])
            self.store[vals[0]] = vals[1]
            # print(vals)
            self.response = 200
            print(self.store)

        print(self.data)
        self.request.send(b'ok')
        self.request.close()
        self.finish()
        # self.request.close

    # def finish(self):
    #     pass




if __name__ == '__main__':

    recurse_server = HTTPServer((HOSTNAME, PORT), Handler)

    print(f'starting server on port {PORT}')
    # print(recurse_server.get_request())
    recurse_server.serve_forever()

