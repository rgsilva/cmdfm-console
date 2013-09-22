import subprocess, signal

EXTERNAL_PLAYER = 'mpg123'
EXTERNAL_PLAYER_ARGS = '-q'

class ExternalPlayer():
	process = None

	def play(self, url):
		if (self.isPlaying()):
			self.stop()

		self.process = subprocess.Popen([EXTERNAL_PLAYER, EXTERNAL_PLAYER_ARGS, url])
		#print("+ Running", EXTERNAL_PLAYER, "with PID", self.process.pid)

	def stop(self):
		self.process.send_signal(signal.SIGTERM)
		self.process = None

	def isPlaying(self):
		if (self.process != None) and (self.process.poll() == None):
			return True
		else:
			return False