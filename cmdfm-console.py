#!/usr/bin/python

import cmd, sys, http.client, json, subprocess, signal

# -----------------------------------------
# Constants

CLIENT_ID		= '?client_id=2b659ea66970555922d89ce9c07b2d0d'
DOMAIN 			= 'cmd.fm'
REQUEST_GENRES	= '/get.php?all_genres=1'
REQUEST_PLAY	= '/get.php?genre='

EXTERNAL_PLAYER = 'mpg123'
EXTERNAL_PLAYER_ARGS = '-q'

# -----------------------------------------
# HTTP stuff

class HttpConnection():
	connection = None

	def __init__(self, domain):
		self.connection = http.client.HTTPConnection(domain)

	def json(self, url):
		self.connection.request('GET', url)
		response = self.connection.getresponse()
		data = response.read().decode('ascii')

		return json.loads(data)

# -----------------------------------------
# Playback stuff

class ExternalPlayer():
	process = None

	def play(self, url):
		if (self.process != None):
			self.stop()

		self.process = subprocess.Popen([EXTERNAL_PLAYER, EXTERNAL_PLAYER_ARGS, url])
		print("+ Running", EXTERNAL_PLAYER, "with PID", self.process.pid)

	def stop(self):
		self.process.send_signal(signal.SIGTERM)
		self.process = None

# -----------------------------------------
# Command-line interface

class Console(cmd.Cmd):
	http = None
	player = None

	# --- Internal code ---

	def prepare(self, http, player):
		self.http = http
		self.player = player

	# --- Basic functions ---

	def do_about(self, args):
		print('TODO about')

	def do_exit(self, arg):
		return True

	# --- cmd.fm functions ---

	def do_genre(self, args):
		if (args == 'list'):
			genres = self.http.json(REQUEST_GENRES)
			for g in genres:
				print("  -", g)

	def do_play(self, genre):
		info = self.http.json(REQUEST_PLAY + genre)

		print('+ Playing', info['title'])
		self.player.play(info['stream_url'] + CLIENT_ID)

	def do_stop(self, genre):
		self.player.stop()

# -----------------------------------------
# General code

def startup():
	player = ExternalPlayer()
	http = HttpConnection(DOMAIN)

	console = Console()
	console.prepare(http, player)
	console.cmdloop()

if __name__ == '__main__':
	startup()
