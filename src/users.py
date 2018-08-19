#!/usr/bin/env python3
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


def is_user_and_password_given(args):
    return True if args.u and args.p else False


def list_parse(args):
    if args.list:
        print("Users list:")
        for user in User.load_all_users():
            print(f"\t{user}")


if __name__ == '__main__':
    args = parse_arguments()
    list_parse(args)
