import sys
import math
import random
import requests

from settings import API_KEY

class APIWrapper():
	def __init__(self):
		self.key = API_KEY
		self.base = 'http://api.themoviedb.org/3'

	def craft(self, chunk):
		return '%s%s?api_key=%s' % (self.base, chunk, self.key)

	def get_genres(self):
		r = requests.get(self.craft('/genre/movie/list'))
		return r.json()['genres']

	def discover(self, genre_id):
		r = requests.get('%s&with_genres=%s' % (self.craft('/discover/movie'), genre_id))
		return r.json()

class MovieManager():

	commands = ['genres', 'next']

	def __init__(self):
		self.api = APIWrapper()
		self._genres = self.api.get_genres()
		self.genre_names = [g['name'].lower() for g in self._genres]

	#HELPERS
	def random(self, _list):
		return _list[int(math.floor(random.random() * len(_list)))]

	# COMMANDS
	def genres(self, *args):
		print 'Genres'
		print '------'
		for genre in self._genres:
			print genre['name']

	def next(self, genre=None, *args):

		if genre:
			if genre.lower() not in self.genre_names:
				print 'That genre does not exist. Use the "genres" command to find out what is available.'
				return

			genre = [g for g in self._genres if g['name'].lower() == genre.lower()][0]
		else:
			print 'No genre specified. Picking a random genre.'
			genre = self.random(self._genres)
			print 'Genre: %s' % genre['name']

		genre_id = genre['id']
		movie_list = self.api.discover(genre_id)['results']
		movie = self.random(movie_list)

		print 'The next movie you should watch is "%s"' % movie['title']

manager = MovieManager()

command = sys.argv[1]

if command not in manager.commands:
	print '"%s" is not a valid command.' % command
	sys.exit()

getattr(manager, command)(*sys.argv[2:])
