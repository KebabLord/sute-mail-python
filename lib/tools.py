""" This module includes some static functions """
import secrets
import string
import re
from inspect import cleandoc
from random import randint
import sys
import argparse
import requests
from requests.exceptions import ConnectionError as rConnectionError, Timeout, ConnectTimeout
from bs4 import BeautifulSoup as bs4
from colorama import Fore,Style

from .config import Files

class MailTools:
    @staticmethod
    def read_mail(mail):
        """
        Parse mail html.
        First gets the solid text, then prints the buttons with links and titles.
        """
        print(f"{Style.BRIGHT}Title:{Style.RESET_ALL}",mail.title)
        print(f"{Style.BRIGHT}From:{Style.RESET_ALL}",mail.sender)
        soup = bs4(mail.text,"html.parser")
        raw = soup.get_text()
        text = '\n'.join([x for x in raw.splitlines() if x.strip()])
        # Remove first line because it's duplicate of title.
        text = text[text.index("\n")+1:]
        print(text+"\n")
        # Get buttons and links
        linx = soup.findAll('a', attrs={'href': re.compile("^http[s,]://")})
        for i in linx:
            prefix = (f"{Style.BRIGHT}{Fore.GREEN}({i.getText().strip()})↴{Style.RESET_ALL}\n","")
            prefix = prefix[ i.getText() == '' ]
            print(prefix+PrtTools.decrypt_url(i.get("href")))

    @staticmethod
    def find_mailbox(val,box=None):
        """
        Find mailbox from given search pattern, if digit, use it as index
        If string, search it on mail addresses. Also if box is not passed
        search it on cached index instead.
        Ex:
          find_mailbox("1",box) -> returns mails[1]
          find_mailbox("usagi",box) -> returns "usagimo321@example.co"
        """
        try:
            if box:
                if val.isdigit():
                    return box.mails[int(val)-1]
                return [i for i in box.mails if val in i.address][0]
            #Use Cache instead if box is not specified.
            with open(Files.mailboxes,"r") as file:
                mails = file.read().strip().split("\n")
            if val.isdigit():
                return mails[int(val)-1]
            return [i for i in mails if val in i][0]
        except IndexError:
            print("Mail couldn't found.")
            sys.exit(1)

class PrtTools:
    @staticmethod
    def gen_details(password=None,nick=None):
        """ Generate safe passwords and random usernames """
        if password:
            chars = string.digits + string.ascii_letters + "#$%&@?=.;:"
            return ''.join(secrets.choice(chars) for i in range(15))
        if nick:
            nick =''.join(secrets.choice(string.ascii_lowercase) for i in range(6))
            return nick+str(randint(0,999))
        return None

    @staticmethod
    def escape_ansi(var):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', var)

    @staticmethod
    def clear_line():
        print('\033[2K\033[1G',end="\r")

    @staticmethod
    def decrypt_url(url):
        """ Decrypt redirect url by parsing metadata of gateaway. """
        print("Trying to decrypt gateaway urls..",end="\r")
        try:
            req = requests.get(url)
            PrtTools.clear_line()
            return re.findall('href = "(.*)"',req.text)[0]
        except (Timeout, ConnectTimeout,rConnectionError):
            PrtTools.clear_line()
            return url

class Params:
    """ Register parameters and subcommands """
    parser = None
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(dest="command")
        subparsers.required = True
        comm_read = subparsers.add_parser("read",help="Read mails")
        comm_read.add_argument("--address","-a", required=False,
            help="Select address from it's index or name")
        comm_read.add_argument("--last","-l", required=False,
            help="Select latest mail",action="store_true")

        comm_del = subparsers.add_parser("del",help="Delete a mailbox")
        comm_del.add_argument("--address","-a",  required=True,
            help="Select address from it's index or name")

        subparsers.add_parser("list",help="List mail addresses")
        subparsers.add_parser("create",help="Create new random address")

        comm_gen = subparsers.add_parser("gen",
            help="Generate random usernames/passwords and save them")
        comm_gen.add_argument(
            "--address","-a", required=True,help="Select address from it's index or name")
        comm_gen.add_argument(
            "--save","-s",    required=False, help="Save account details with specified tag")
        comm_gen.add_argument(
            "--password","-p",required=False, help="Generate password",action="store_true")
        comm_gen.add_argument(
            "--uname","-u",   required=False, help="Generate username",action="store_true")
        comm_gen.add_argument(
            "--wait","-w",   required=False, help="Start listening mails",action="store_true")

        comm_w8 = subparsers.add_parser("wait",help="Wait for new mails")
        comm_w8.add_argument("--address","-a",  required=True,
            help="Select address from it's index or name")

        custom_help = cleandoc(
            """Takoyaki is an interactive burner mail creator and controller.
            Usage:
              takoyaki [COMMAND] [ARGS...]
              takoyaki -h | --help

            Commands:
              create [-h]               Create new random mail address
              read   [-hal]             Read mails from specified address
              wait   [-ha]              Wait for new mails on specified address
              del    [-ha]              Delete specified mail address
              list   [-h]               List current mail addresses
              gen    [-hwpusa]          Generate registration details

            Options:
              -h, --help                Show extended information about the subcommand
              -a, --address <ADDRESS>   Specify the mail address
              -l, --last                Select latest mail
              -p, --password            Generate password
              -u, --uname               Generate username
              -w, --Wait                Start listening new mails after generate
              -s, --save <NAME>         Save generated info to .accs file
            """)+"\n"
        self.parser.format_help = custom_help.__str__
