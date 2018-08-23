#!/usr/bin/env python3
import sys
import argparse
from models.User import User


def parse_arguments():
    parser = argparse.ArgumentParser()
    exclusive_group = parser.add_mutually_exclusive_group()
    parser.add_argument('-u', '--username', help='user login')
    parser.add_argument('-p', '--password', help='user password')
    exclusive_group.add_argument('-l', '--list', action='store_true', help='list all users')
    exclusive_group.add_argument('-d', '--delete', action='store_true', help='delete user')
    exclusive_group.add_argument('-n', '--new-pass', help='new user password')
    exclusive_group.add_argument('-e', '--edit', help='edit user login')
    parser.add_argument('-c', '--confirm', help='confirm password for new created user \n'
                                                'or confirm new password for existing user \n'
                                                'or confirm new login \n'
                                                'or confirm login for deleted user')
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


def create_user(args):
    if not args.confirm:
        raise ValueError("-c (--confirm) parameter with repeated password (-p or -password argument) is required.")
    elif not args.confirm == args.password or len(args.password) < 8:
        raise ValueError("confirm password do not match to password or password is shorter than eight characters.")
    else:
        new_user = User()
        new_user.username = args.username
        new_user.hashed_password = args.password
        return new_user.save_to_db()


def list_parse(args):
    if args.list:
        print("Users list:")
        for user in User.load_all_users():
            print(f"\t{user}")
        sys.exit()


if __name__ == '__main__':
    args = parse_arguments()
    list_parse(args)
    if parse_user_and_password(args):
        user = User.load_user_by_name(args.username)
        if args.delete:
            if args.confirm == args.username:
                user.delete()
                print(f"User '{args.username}' deleted.")
            else:
                raise ValueError("-c (--confirm) argument with repeated user login has to be given "
                                 "then tne user with this login will be deleted")
        elif args.edit:
            if args.confirm == args.edit:
                user.username = args.edit
                user.save_to_db()
            else:
                raise ValueError("-c (--confirm) argument with repeated edit argument has to be given "
                                 "then the new user login will be saved")
        elif args.new_pass:
            if args.confirm == args.new_pass:
                user.set_new_password(old_pass=args.password, old_pass_hashed=user.hashed_password,
                                      new_pass=args.new_pass, new_pass_confirm=args.confirm)
                user.save_to_db()
                print(f"Password for user '{args.username}' changed.")
            else:
                raise ValueError("-c (--confirm) argument with repeated new_pass argument has to be given "
                                 "then the new user password will be saved")
