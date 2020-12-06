#!/usr/bin/env python3
"""Takoyaki is a script to create instant burner accounts."""
from os.path import exists
import sys
from PyInquirer import prompt
from requests.exceptions import Timeout, ConnectTimeout
import tools
from sute import Sute

args = tools.parser.parse_args()
Colors = tools.Colors

def connect():
    try:
        print("Connecting..",end="\r")
        if exists(".ses"):
            with open(".ses") as ses_file:
                ses_id = ses_file.read()
        else:
            ses_id = None
        sute = Sute(ses_id=ses_id)
        tools.clearLine()
        with open(".mails","w") as cache:
            cache.writelines([mail.address+"\n" for mail in sute.mails])
        return sute
    except (ConnectionError, Timeout, ConnectTimeout):
        print("Connection problem.")
        sys.exit(1)

if args.command in ["del","read","create","list","wait"]:
    box=connect()

if args.command == "create":
    new = box.create_new_random_address()
    print("created:",new.address)
    with open(".mails","w") as f:
        f.writelines([mail.address+"\n" for mail in box.mails])

elif args.command == "list":
    box.refresh_address_list()
    for x,y in enumerate(box.mails):
        print("{}  {}".format(x+1,y.address))

elif args.command == "gen":
    if exists(".mails"):
        selected_mail=tools.find_mailbox(args.address)
    else:
        box = connect()
        selected_mail=tools.find_mailbox(args.address,box).address

    result=f"{Colors.BOLD}Mail:{Colors.ENDC} {selected_mail} \n"
    if args.uname:
        result+=f"{Colors.BOLD}Nick:{Colors.ENDC} {tools.gen_nick()} \n"
    if args.password:
        result+=f"{Colors.BOLD}Pass:{Colors.ENDC} {tools.gen_password()} \n"
    if args.save:
        result=f"{Colors.BOLD}=== {args.save.title()} Account ==={Colors.ENDC}\n"+result
        with open(".accs","a") as f:
            f.write(result+"\n")
    print(result)

elif args.command == "del":
    mailbox = tools.find_mailbox(args.address,box)
    status = mailbox.delete_mailbox()
    if status==200:
        print("Success.")

elif args.command == "read":
    if args.address:
        selected_mailbox = tools.find_mailbox(args.address,box)
        pass
    else:
        selected_mailbox = prompt([{
            'type': 'list',
            'name': 'mailbox',
            'message': 'Select mailbox',
            'choices': [{a:b for a,b in (("name",i.address),("value",i))} for i in box.mails]
            }])["mailbox"]

    mails = selected_mailbox.get_mail_list()
    mail_list=[{a:b for a,b in (("name",i.title),("value",i))} for i in mails]
    if mail_list:
        selected_mail = prompt([{
            'type': 'list',
            'name': 'mail',
            'message': 'Select mail',
            'choices':  mail_list
            }])["mail"]
        tools.read_mail(selected_mail)
    else:
        print("No mails.")
elif args.command == "wait":
    selected_mailbox = tools.find_mailbox(args.address,box)
    print(f"Waiting new mails for {selected_mailbox.address}")
    mails=selected_mailbox.get_mail_list()
    print(f"Last mail was: {mails[0]}\nPress Ctrl+C to Abort.",end="\r")
    count = cur_count = len(mails)
    while count == cur_count:
        try:
            mails=selected_mailbox.get_mail_list()
            cur_count = len(mails)
        except KeyboardInterrupt:
            print('Aborted.')
            sys.exit()
        except (ConnectionError, Timeout, ConnectTimeout):
            pass
    tools.clearLine()
    tools.read_mail(mails[0])
