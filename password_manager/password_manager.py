import sys
import getpass
import pickle
import random
import string

from simplecrypt import encrypt, decrypt
from passlib.hash import sha256_crypt

class PasswordManager():

	filename = 'secret_password_file.txt'
	password = ''

	commands = ['add', 'remove', 'get', 'list']
	filedata = {}

	def __init__(self):
		self.prepare_password_file()
		self.password_check()

	def create_file(self):
		f = open(self.filename, 'a')
		f.close()

	@property
	def is_password_set(self):
		return self.filedata.get('password')

	@property
	def password_hash(self):
		return self.filedata.get('password')

	def prepare_password_file(self):
		self.create_file()

		with open(self.filename, 'r') as f:
			try:
				self.filedata = pickle.load(f)
			except Exception as e:
				self.filedata = {}

	def save(self):
		with open(self.filename, 'w') as f:
			pickle.dump(self.filedata, f)

	def hash_password(self, password):
		return sha256_crypt.encrypt(password)

	def verify_password(self, password):
		return sha256_crypt.verify(password, self.password_hash)

	def encrypt_password(self, secret, password):
		return encrypt(secret, password)

	def decrypt_password(self, secret, encrypted):
		return decrypt(secret, encrypted)

	def random_string(self, len=12):
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))

	def password_check(self):
		if not self.is_password_set:
			password = getpass.getpass('Please enter a password for first time use: ')
			matching_password = getpass.getpass('Confirm password: ')

			if not password == matching_password:
				print 'Passwords do not match!'
				return self.password_check()

			password_hash = self.hash_password(password)
			self.filedata['password'] = password_hash

		else:
			password = getpass.getpass('Enter your password manager password: ')

			if not self.verify_password(password):
				print 'Incorrect password!'
				return self.password_check()

		self.password = password

	def add(self, website, *args):
		password = self.random_string()

		if website in self.filedata.keys():
			print 'Error: %s already exists' % website
			return

		self.filedata[website] = self.encrypt_password(self.password, password)
		print 'Your new password is %s' % password

	def get(self, website, *args):
		encrypted = self.filedata.get(website)

		if not encrypted:
			print 'Error: no password set for %s' % website

		password = self.decrypt_password(self.password, encrypted)
		print 'Password for %s: %s' % (website, password)

	def remove(self, website, *args):
		if website not in self.filedata.keys():
			print 'Error: %s does not exist' % website
			return

		del self.filedata[website]
		print 'Successfully removed %s' % website

	def list(self, *args):
		print ''
		print 'Websites'
		print '--------'
		for key in self.filedata.keys():
			if key != 'password':
				print key
		print ''

manager = PasswordManager()

command = sys.argv[1]

if command not in manager.commands:
	print '"%s" is not a valid command.' % command
	sys.exit()

getattr(manager, command)(*sys.argv[2:])
manager.save()

