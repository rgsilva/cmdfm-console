import http.client, json, urllib.parse

class HttpEngine():
	connection = None

	def __init__(self, domain):
		self.connection = http.client.HTTPConnection(domain)	

	# -----------------------------------------
	# General functions

	def escape(self, str):
		return urllib.parse.quote_plus(str)

	# -----------------------------------------
	# Connection-related functions

	def reconnect(self):
		try:
			self.connection.close()
		except:
			# Do nothing if it fails to close - we're reconnecting anyway.
			None

		self.connection.connect()

	# -----------------------------------------
	# Request functions

	def json(self, url):
		try:
			self.connection.request('GET', url)
			response = self.connection.getresponse()
			data = response.read().decode('ascii')

			return json.loads(data)
		except (http.client.BadStatusLine, http.client.CannotSendRequest):
			self.reconnect()
			return self.json(url)
		except:
			print('- Something went quite wrong inside this application.')
			print('- Sit down and relax as it tries to fix itself!')
			self.reconnect()
			return self.json(url)