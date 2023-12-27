import argparse

from . import install_soroban
from . import install_app
from . import deploy
from . import invoke


def parseCommand():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', type=str)

    args, _ = parser.parse_known_args()

    if args.action == 'install-app':
        parser.add_argument(
            'target', type=str, help='Must be "standalone", "astro" or "nextjs"')
        parser.add_argument('name', type=str, help='Name of the app')
    elif args.action == 'deploy':
        parser.add_argument("-n", "--network", default=None,
                            help="Specify the network")
    elif args.action == 'invoke':
        parser.add_argument('function', type=str,
                            help='Name of the fuction to call')
        parser.add_argument("-a", "--args", default="",
                            help="Arguments to pass to the function call")
        parser.add_argument("-n", "--network", default=None,
                            help="Specify the network")

    return parser.parse_args()


def main():
    args = parseCommand()

    if args.action == 'install-soroban':
        install_soroban.install_soroban()

    elif args.action == 'install-app':
        if args.target == 'standalone':
            install_app.install_standalone_app(args.name)
        elif args.target == 'astro':
            install_app.install_astro_app(args.name)
        elif args.target == 'nextjs':
            install_app.install_nextjs_app(args.name)

    elif args.action == 'deploy':
        deploy.deploy(args.network)

    elif args.action == 'invoke':
        invoke.invoke_with_str(args.function, args.args, args.network)

    else:
        print('Unknown command')


main()
