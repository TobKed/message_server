import argparse
from models.User import User


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='user login')
parser.add_argument('-p', '--password', help='user password')
parser.add_argument('-n', '--new-pass', help='new user password')
parser.add_argument('-l', '--list', help='list all users')
parser.add_argument('-d', '--delete', help='delete user by login')
parser.add_argument('-e', '--edit', help='edit user by login')
args = parser.parse_args()
