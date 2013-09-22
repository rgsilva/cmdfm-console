import http.client, json

class HttpConnection():
	connection = None

	def __init__(self, domain):
		self.connection = http.client.HTTPConnection(domain)	

	def reconnect(self):
		try:
			self.connection.close()
		except:
			# Do nothing if it fails to close - we're reconnecting anyway.
			None

		self.connection.connect()

	def json(self, url):
		self.connection.request('GET', url)
		response = self.connection.getresponse()
		data = response.read().decode('ascii')

		return json.loads(data)
