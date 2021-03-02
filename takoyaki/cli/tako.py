#!/usr/bin/env python3
"""Takoyaki is a script to create instant burner accounts."""
from takoyaki.tools import Params
from takoyaki import Takoyaki

def main():
    params = Params()
    args = params.parser.parse_args()
    yaki = Takoyaki()

    if args.command in ["del","read","create","list","wait"]:
    # if one of the commands above, connect automatically
        yaki.connect()

    if args.command == "create":
        yaki.create()

    elif args.command == "list":
        yaki.list()

    elif args.command == "gen":
        yaki.gen()

    elif args.command == "del":
        yaki.delete()

    elif args.command == "read":
        yaki.read()

    elif args.command == "wait":
        yaki.wait()

if __name__ == "__main__":
    main()
