"""Command line for testing"""
import argparse
import functools
import json
from tornado import ioloop
from . import pyfb


def cmdline(args=None):
    """Command line"""
    parsers = {}
    parsers['main'] = argparse.ArgumentParser(
        description='Pyfb command line'
    )
    parsers['main'].add_argument(
        'app_id', type=str, help='Facebook app ID'
    )
    parsers['command'] = parsers['main'].add_subparsers(
        title="Commands", dest='command'
    )
    parsers['user'] = parsers['command'].add_parser(
        'user', help='User / account commands'
    )
    parsers['user'].add_argument(
        'user_access_token', type=str, help='User access token'
    )
    parsers['user_command'] = parsers['user'].add_subparsers(
        title="User command", dest='user_command'
    )
    parsers['user_self'] = parsers['user_command'].add_parser(
        'self', help='Get user self'
    )
    parsers['user_friends'] = parsers['user_command'].add_parser(
        'friends', help='Get user friend list (all or app, default app)'
    )
    parsers['user_friends'].add_argument(
        '--friend_type', default='app', help='Friend type'
    )
    args = parsers['main'].parse_args(args)
    fun = None
    fb = pyfb.Pyfb(args.app_id, raw_data=True)
    if args.command == 'user':
        fb.set_access_token(args.user_access_token)
        if args.user_command == 'self':
            fun = fb.get_myself
        elif args.user_command == 'friends':
            fun = functools.partial(
                fb.get_friends, friend_type=args.friend_type
            )
    if fun is not None:
        data = ioloop.IOLoop.current().run_sync(fun)
        print(json.dumps(data, indent=2))

if __name__ == '__main__':
    cmdline()
