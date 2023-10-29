"""
MIT License

Copyright (c) 2023 Jakob Felix Rieckers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import argparse
import json
import stupidArtnet
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import tkinter.filedialog

    tkinter_imported = True
except:
    print("Couldn't import tkinter")
    tkinter_imported = False

# own modules
import Calculator

FAVICON_PATH = "webserver_files/favicon.ico"
INDEX_PATH = "webserver_files/index.html"
SCRIPT_PATH = "webserver_files/scripts.js"
with open("known_lights.json") as f:
    KNOWN_LIGHTS = json.load(f)

room_view_path = ""
json_data = None
artnet_class = None


# HTTP Server stuff
class WebServer(BaseHTTPRequestHandler):
    def _set_html_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404!</h1><br><h2>Sorry...</h2></body></html>")

    def _send_favicon(self):
        with open(FAVICON_PATH, "rb") as f:
            favicon_data = f.read()
        self.send_response(200)
        self.send_header('Content-type', 'image/x-icon')
        self.end_headers()
        self.wfile.write(favicon_data)

    def _send_room_view(self):
        if not room_view_path:
            self._send_404()
            return
        with open(room_view_path, "rb") as f:
            room_view = f.read()
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(room_view)

    def _send_index_view(self):
        with open(INDEX_PATH, "rb") as f:
            room_view = f.read()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(room_view)

    def _send_script(self):
        with open(SCRIPT_PATH, "rb") as f:
            script = f.read()
        self.send_response(200)
        self.send_header('Content-type', 'text/javascript')
        self.end_headers()
        self.wfile.write(script)

    def do_GET(self):
        if self.path in ["/index.html", "/"]:
            self._send_index_view()
        elif self.path == "/room_view.png":
            self._send_room_view()
        elif self.path == "/favicon.ico":
            self._send_favicon()
        elif self.path == "/scripts.js":
            self._send_script()
        else:
            self._send_404()

    def do_POST(self):
        global artnet_class
        self._set_html_headers()
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode("utf-8")
        post_data = json.loads(post_body)
        if artnet_class:
            artnet_class.send_data(*post_data.values())
        self.wfile.write(b"<html><body><h1>POST Request Received!</h1></body></html>")

    def log_message(self, format, *args):
        pass


def run_server(port, server_class=HTTPServer, handler_class=WebServer):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running at localhost:{port}...')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Stopped")


# stupidArtNet stuff
class ArtNetClient:
    def __init__(self, event_data, target_ip: str = "127.0.0.1", universe: int = 1, packet_size: int = 512):
        self.dmx_data = [0] * packet_size
        self.event_data = event_data
        print("Known lights:", KNOWN_LIGHTS)
        self.artnet_client = stupidArtnet.StupidArtnet(target_ip=target_ip, universe=universe, packet_size=packet_size)

    def send_data(self, x_p, y_p, z):  # x and y as a percentage and z as a number in centimeter
        x = self.event_data["room"][0] * x_p / 100
        y = self.event_data["room"][1] * y_p / 100

        for light in self.event_data["lights"]:
            known_light = KNOWN_LIGHTS[light["knownLight"]]
            pan_a, tilt_a = Calculator.calculate(*light["position"], x, y, z, light["panOrientation"])
            pan, pan_fine, tilt, tilt_fine = Calculator.angles_to_dmx_values(known_light["minPan"],
                                                                             known_light["maxPan"],
                                                                             known_light["minTilt"],
                                                                             known_light["maxTilt"], pan_a, tilt_a,
                                                                             known_light["hasFine"])
            if known_light["hasFine"] and light["fine"]:
                start_address = known_light["channelsStartFine"] + light["address"] - 1
                self.dmx_data[start_address: start_address+4] = [pan, pan_fine, tilt, tilt_fine]
            else:
                start_address = known_light["channelsStart"] + light["address"] - 1
                self.dmx_data[start_address: start_address+2] = [pan, tilt]
        self.send()

    def send(self):
        self.artnet_client.set(bytearray(self.dmx_data))
        self.artnet_client.show()


# other stuff
def get_file_with_dialog(title, filetypes):
    if not tkinter_imported:
        raise ModuleNotFoundError("Please install Tkinter or try: 'python3 InitSetupEvent.py --help'")
    return tkinter.filedialog.askopenfilename(title=title, filetypes=filetypes)


def main():
    global room_view_path, json_data, artnet_class
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "-i", "--image", help="the base image for your web browser", dest="image")
    arg_parser.add_argument("-ad", "--all-data", help="filepath for a json file with all data in it.", dest="json_file")
    arg_parser.add_argument("--port", help="port for the webserver", type=int, default=5120, dest="port")
    args = arg_parser.parse_args()

    if args.json_file:
        json_path = args.json_file
    else:
        json_path = get_file_with_dialog("Select your data file", (("json files", "*.json"), ("all files", "*.*")))
    with open(json_path) as f:
        json_data = json.load(f)

    if args.image:
        room_view_path = args.image
    else:
        room_view_path = get_file_with_dialog("Select your base image",
                                              (("Image files", "*.png"), ("all files", "*.*")))

    artnet_class = ArtNetClient(json_data, target_ip="127.255.255.255")
    run_server(port=args.port)


if __name__ == "__main__":
    main()
else:
    raise ImportError("This is not a module")
