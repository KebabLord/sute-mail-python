import secrets,string
from bs4 import BeautifulSoup as bs4
import sute,re,requests
from random import randint
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command",required=True)

comm_read = subparsers.add_parser("read",help="Read mails")
comm_read.add_argument("--address","-a", required=False,help="Select address from it's index or name")

comm_del = subparsers.add_parser("del",help="Delete a mailbox")
comm_del.add_argument("--address","-a",  required=True, help="Select address from it's index or name")

comm_list = subparsers.add_parser("list",    help="List mail addresses")
comm_create = subparsers.add_parser("create",help="Create new random address")

comm_gen = subparsers.add_parser("gen", help="Generate random usernames/passwords and save them")
comm_gen.add_argument("--address","-a", required=True,  help="Select address from it's index or name")
comm_gen.add_argument("--save","-s",    required=False, help="Save account details with specified tag")
comm_gen.add_argument("--password","-p",required=False, help="Generate password",action="store_true")
comm_gen.add_argument("--uname","-u",   required=False, help="Generate username",action="store_true")

comm_w8 = subparsers.add_parser("wait",help="Poop fart")
comm_w8.add_argument("--address","-a")

def custom_help(): return """Kuku 1.0, an interactive burner mail creator and controller.
Usage: kuku [SUBCOMMAND] [OPTION]...

subcommands:
  create [-h]               Create new random mail address
  read   [-ha]              Read mails from specified address
  del    [-ha]              Delete specified mail address
  list   [-h]               List current mail addresses
  gen    [-hpuas]           Generate registration details

parameters:
  -h, --help                Show extended information about the subcommand
  -a, --address <ADDRESS>   Specify the mail address
  -p, --password            Generate password
  -u, --uname               Generate username
  -s, --save <NAME>         Save generated info to .accs file
"""
parser.format_help = custom_help


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clearLine():
    print('\033[2K\033[1G',end="\r")

def decryptURL(url): # Decrypt redirect url by parsing metadata of gateaway.
    print("Trying to decrypt gateaway urls..",end="\r")
    try:
        req = requests.get(url)
        clearLine()
        return re.findall('href = "(.*)"',req.text)[0]
    except:
        clearLine()
        return url

def read_mail(mail):
    print(f"{colors.BOLD}Title:{colors.ENDC}",mail.title)
    print(f"{colors.BOLD}From:{colors.ENDC}",mail.sender)
    # Get the text
    soup = bs4(mail.text,"html.parser")
    raw = soup.get_text()
    text = '\n'.join([x for x in raw.splitlines() if x.strip()])
    text = text[text.index("\n")+1:] # Remove first line because it's duplicate of title.
    print(text+"\n")
    # Get buttons and links
    linx = soup.findAll('a', attrs={'href': re.compile("^http[s,]://")})
    for i in linx:
        prefix = (f"{colors.BOLD}{colors.OKGREEN}({i.getText().strip()})↴{colors.ENDC}\n","")[ i.getText() == '' ]
        print(prefix+decryptURL(i.get("href")) )

def find_mailbox(val,box=None):
    try:
        if box: 
            if val.isdigit():
                return box.mails[int(val)-1]
            else:
                return [i for i in box.mails if val in i.address][0]
        else:
            with open(".mails","r") as f:
                mails = f.read().strip().split("\n")
            if val.isdigit():
                return mails[int(val)-1]
            else:
                return [i for i in mails if val in i][0]
    except:
        print("Mail couldn't found.")
        exit(1)

def gen_password():
    chars = string.digits + string.ascii_letters + "#$%&@?=.;:"
    return ''.join(secrets.choice(chars) for i in range(15)) # 15 being password length

def gen_nick(): 
    nick =''.join(secrets.choice(string.ascii_lowercase) for i in range(6)) # 15 being password length
    return nick+str(randint(0,999))

def escapeANSI(var):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', var)
