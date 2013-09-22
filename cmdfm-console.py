#!/usr/bin/python

import cmd, sys, threading

from ExternalPlayer import *
from HttpEngine import *

# -----------------------------------------
# Constants

CHECK_INTERVAL			= 3

DOMAIN 					= 'cmd.fm'
REQUEST_GENRES_LIST		= '/get.php?all_genres=1'
REQUEST_GENRES_SEARCH	= '/get.php?genres=1&q='
REQUEST_PLAY			= '/get.php?genre='

CLIENT_ID				= '?client_id=2b659ea66970555922d89ce9c07b2d0d'

# -----------------------------------------
# Command-line interface

class Console(cmd.Cmd):
	http = None
	player = None
	timer = None

	prompt = '(cmd.fm) '

	# --- Internal code ---

	def prepare(self, http, player):
		self.http = http
		self.player = player

	def check_playback(self):
		# If our last song has finished and we still have a genre, repeat it.
		if (self.last_genre != None) and (not self.player.isPlaying()):
			# Let's repeat the last genre.
			self.do_play(self.last_genre)
		else:
			# Just reset our timer.
			self.timer = threading.Timer(CHECK_INTERVAL, self.check_playback)
			self.timer.start()

	# --- Console controls ---

	def emptyline(self):
		return False

	# --- Basic functions ---

	def do_about(self, args):
		print('  * * * * * * * * * * * * * * * * * * * * * * *')
		print('  *                                           *')
		print('  * cmd.fm console                            *')
		print('  *                                           *')
		print('  * https://github.com/rgsilva/cmdfm-console  *')
		print('  *                                           *')
		print('  * * * * * * * * * * * * * * * * * * * * * * *')

	def do_exit(self, args):
		if (self.player.isPlaying()):
			self.player.stop()

		print('Bye!')
		return True

	def do_help(self, args):
		print('Available commands are')
		print('---------------------------------------------------------')
		print('genre list               # Lists all genres')
		print('genre search <query>     # Search genre')
		print('play <genre name>        # Play genre tracks')
		#print('status                   # Shows track status')
		#print('resume                   # Resume playback')
		#print('pause                    # Pause playback')
		print('skip                     # Skip current track')
		print('about                    # Hello?')
		print('---------------------------------------------------------')

	# --- cmd.fm functions ---

	# genre list
	# genre search <keyword>
	def do_genre(self, args):
		url = None

		if (args == 'list'):
			url = REQUEST_GENRES_LIST
		elif (args.split()[0] == 'search'):
			keyword = ' '.join(args.split()[1:])
			if (keyword == ''):
				print('- You need to specify a keyword to look for.')
				return False

			url = REQUEST_GENRES_SEARCH + self.http.escape(keyword)
		else:
			print("- Invalid usage.")
			return False

		genres = self.http.json(url)
		for g in genres:
			print("-", g)

	# play <genre>
	def do_play(self, genre):
		if (genre == ''):
			print("- You need to specify a genre.")
			return False

		# Get the stream information.
		info = self.http.json(REQUEST_PLAY + self.http.escape(genre))

		# Just in case.
		if (info == False):
			print("- The genre you specified is invalid.")
			return False

		# We got a song, so let's stop our timer, just in case.
		if (self.timer != None):
			self.timer.cancel()

		# Play it.
		try:
			self.player.play(info['stream_url'] + CLIENT_ID)
			print('+ Playing', info['title'])

			# Save the genre for repeating
			self.last_genre = genre

			# Start the timer.
			self.check_playback()
		except:
			print("- Something went wrong with the playback. Please try again.")

	# stop
	def do_stop(self, args):
		if (self.player.isPlaying()):
			self.last_genre = None
			self.player.stop()
		else:
			print('- Cannot stop a song that\'s not playing!')
			return False

	# skip
	def do_skip(self, args):
		if (self.player.isPlaying()):
			self.player.stop()
			self.do_play(self.last_genre)
		else:
			print('- Cannot skip a song that\'s not playing!')
			return False

# -----------------------------------------
# General code

def startup():
	player = ExternalPlayer()
	http = HttpEngine(DOMAIN)

	console = Console()
	console.prepare(http, player)
	console.cmdloop()

if __name__ == '__main__':
	startup()
