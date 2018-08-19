#!/usr/bin/env python3
import sys
import argparse
from models.User import User


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='user login')
    parser.add_argument('-p', '--password', help='user password')
    parser.add_argument('-n', '--new-pass', help='new user password')
    parser.add_argument('-l', '--list', action='store_true', help='list all users')
    parser.add_argument('-d', '--delete', action='store_true', help='delete user by login')
    parser.add_argument('-e', '--edit', action='store_true', help='edit user by login')
    return parser.parse_args()


def parse_user_and_password(args):
    if args.username and args.password:
        user = User.load_user_by_name(args.username)
        if user:
            if User.check_password(args.password, user.hashed_password):
                return True
            else:
                print("Wrong password!")
        else:
            print(f"No user '{args.username}' in the database.")
            create_user(args.username)
    else:
        print("-u (--user) and -p (--password) must be given together.")


def create_user(username):
    #TODO
    pass


def list_parse(args):
    if args.list:
        print("Users list:")
        for user in User.load_all_users():
            print(f"\t{user}")
        sys.exit()


if __name__ == '__main__':
    args = parse_arguments()
    list_parse(args)
    parse_user_and_password(args)
