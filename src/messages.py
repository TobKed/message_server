#!/usr/bin/env python3
import sys
import argparse
from models.User import User
from models.Message import Message


def parse_arguments():
    parser = argparse.ArgumentParser()
    exclusive_group = parser.add_mutually_exclusive_group()
    parser.add_argument('-u', '--username', help='user login')
    parser.add_argument('-p', '--password', help='user password')
    exclusive_group.add_argument('-l', '--list', action='store_true', help='list all users')
    exclusive_group.add_argument('-s', '--send', nargs="+", help='send message')
    parser.add_argument('-t', '--to', help='recipient login')
    return parser.parse_args()


def parse_user_and_password(args):
    if args.username and args.password:
        user = User.load_user_by_name(args.username)
        if user:
            if User.check_password(args.password, user.hashed_password):
                print(f"Correct passowrd for user '{user.username}'.")
                return user
            else:
                raise ValueError("Wrong password!")
        else:
            raise ValueError("No such user in database!")
    elif bool(args.username) != bool(args.password):
        raise ValueError("-u (--user) and -p (--password) arguments must be given together.")


def list_parse(args, user=None):
    if args.list and user:
        print(f" Messages list sent to user '{user.username}':")
        for message in Message.load_all_messages_for_user(user.id):
            print(f"\t{message}")
        print(f" Messages list sent from user '{user.username}':")
        for message in Message.load_all_messages_from_user(user.id):
            print(f"\t{message}")
        sys.exit()
    elif args.list and not user:
        print("All messages list")
        for message in Message.load_all_messages():
            print(f"\t{message}")
        sys.exit()


def send_message(user_from, user_to_username, msg_text):
    user_to = User.load_user_by_name(user_to_username)
    message = Message()
    message.from_id = user_from.id
    message.to_id = user_to.id
    message.msg_text = msg_text
    return message.save_to_db()


if __name__ == '__main__':
    args = parse_arguments()
    user = parse_user_and_password(args)
    list_parse(args, user)
    if user:
        if bool(args.send) != bool(args.to):
            raise ValueError("-s (--send) and -t (--to) arguments must be given together.")
        if args.send and args.to:
            if send_message(user, args.to, " ".join(args.send)):
                print(f"Message from f'{user.id}' to {args.to} was successfully sent")
            else:
                raise RuntimeError("Message was not sent!")
