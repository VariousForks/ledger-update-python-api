from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from ledgerUpdateApi import LedgerUpdateAPI
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
from file_cache import FileCache
from datetime import timedelta

cache = FileCache(timedelta(minutes=10))
api = LedgerUpdateAPI()

class LedgerUpdateHTTPRequestHandler(BaseHTTPRequestHandler):

	endpoints = {
		"/update/firmwares/last": api.getLastFirmware,
		"/update/firmwares": api.getFirmwares,
		"/update/applications": api.getApplications,
		"/update/devices": api.getDevices
	}

	assets = {
		"/update/assets/icons/": ('.png', 'image/png', './assets/icons/')
	}

	def handle_assets(self, path):
		url = urlparse(self.path)
		for key, value in self.assets.items():
			if (path.startswith(key)):
				try:
					f = cache.fetch_bytes(value[2] + path.split('/')[-1] + value[0])
					self.send_response(200)
					self.send_header('Content-type', value[1])
					self.end_headers()
					self.wfile.write(f)
				except Exception as exception:
					answer = api.notFound(self, url.path, parse_qs(url.query))
					self.send_response(answer[0])
					self.send_header('Content-type','application/json')
					self.end_headers()
					self.wfile.write(json.dumps(answer[1]).encode())
				return True
		return False

	def do_GET(self):
		url = urlparse(self.path)

		# Check if we request an asset first
		if (self.handle_assets(url.path) == False):
			# send code 200 response
			answer = self.endpoints.get(url.path, api.notFound)(self, url.path, parse_qs(url.query))

			self.send_response(answer[0])

			#send header first
			self.send_header('Content-type','application/json')
			self.end_headers()

			#send file content to client
			self.wfile.write(json.dumps(answer[1]).encode())
		return

def run():
  print('http server is starting...')
  server_address = ('127.0.0.1', 3001)
  httpd = HTTPServer(server_address, LedgerUpdateHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()

if __name__ == '__main__':
  run()
