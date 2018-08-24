#!/usr/bin/env python3
import sys
import argparse
from models.User import User
from models.Messege import Messege


def parse_arguments():
    parser = argparse.ArgumentParser()
    exclusive_group = parser.add_mutually_exclusive_group()
    parser.add_argument('-u', '--username', help='user login')
    parser.add_argument('-p', '--password', help='user password')
    exclusive_group.add_argument('-l', '--list', action='store_true', help='list all users')
    exclusive_group.add_argument('-s', '--send', help='send messege')
    exclusive_group.add_argument('-t', '--to', help='recipient login')
    return parser.parse_args()


def parse_user_and_password(args):
    if args.username and args.password:
        user = User.load_user_by_name(args.username)
        if user:
            if User.check_password(args.password, user.hashed_password):
                print(f"Correct passowrd for user '{user.username}'.")
                return True
            else:
                raise ValueError("Wrong password!")
        else:
            print(f"No user '{args.username}' in the database.")
            if create_user(args):
                print(f"New user '{args.username}' created.")
    else:
        raise ValueError("-u (--user) and -p (--password) arguments must be given together.")


if __name__ == '__main__':
    args = parse_arguments()
