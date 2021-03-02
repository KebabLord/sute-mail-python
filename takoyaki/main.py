"""Home of main class."""
from os.path import exists
import sys
from questionary import select
from requests.exceptions import ConnectionError as rConnectionError, Timeout, ConnectTimeout
from colorama import Style

from .tools import Params,MailTools,PrtTools
from .sute import Sute
from .config import style,Files

class Takoyaki:
    """ Class that contains main functions """
    def __init__(self):
        self.box = None

    def connect(self):
        """ Creates the mail box object which includes addresses,mails and ids """
        try:
            print("Connecting..",end="\r")
            if exists(Files.ses_token):
                with open(Files.ses_token) as ses_file:
                    ses_id = ses_file.read()
            else:
                ses_id = None
            sute = Sute(ses_id=ses_id)
            PrtTools.clear_line()
            with open(Files.mailboxes,"w") as cache:
                cache.writelines([mail.address+"\n" for mail in sute.mails])
            #return sute
            self.box=sute
        except (Timeout, ConnectTimeout,rConnectionError):
            print("Connection problem.")
            sys.exit(1)

    def list(self):
        self.box.refresh_address_list()
        for i,mail in enumerate(self.box.mails):
            print("{}  {}".format(i+1,mail.address))

    def create(self):
        """ Create a new random burner mail """
        new = self.box.create_new_random_address()
        print("created:",new.address)
        with open(Files.mailboxes,"w") as file:
            file.writelines([mail.address+"\n" for mail in self.box.mails])

    def gen(self):
        """
        Generates a random password and a username
        optionally saves them to 'lib.config.Files.burner_accounts' file with given tag
        """
        if exists(Files.mailboxes):
            selected_mail=MailTools.find_mailbox(args.address)
        else:
            self.connect()
            selected_mail=MailTools.find_mailbox(args.address,self.box).address

        result=f"{Style.BRIGHT}Mail:{Style.RESET_ALL} {selected_mail} \n"
        if args.uname:
            result+=f"{Style.BRIGHT}Nick:{Style.RESET_ALL} {PrtTools.gen_details(nick=True)} \n"
        if args.password:
            result+=f"{Style.BRIGHT}Pass:{Style.RESET_ALL} {PrtTools.gen_details(password=True)} \n"
        if args.save:
            result=f"{Style.BRIGHT}=== {args.save.title()} Account ==={Style.RESET_ALL}\n"+result
            with open(Files.burner_accounts,"a") as file:
                file.write(PrtTools.escape_ansi(result)+"\n")
        print(result)
        if args.wait:
            self.connect()
            self.wait()

    def delete(self):
        mailbox = MailTools.find_mailbox(args.address,self.box)
        status = mailbox.delete_mailbox()
        if status==200:
            print("Success.")

    def read(self):
        """ Read mails, prompts interactive cli if target mail box is not specified """
        if args.address:
            selected_mailbox = MailTools.find_mailbox(args.address,self.box)
        else:
            selected_mailbox = select(
                "Select mailbox",
                choices=[{a:b for a,b in (("name",i.address),("value",i))}
                              for i in self.box.mails],
                style=style,
                instruction=" "
            ).ask()

        mails = selected_mailbox.get_mail_list()
        mail_list=[{a:b for a,b in (("name",i.title),("value",i))} for i in mails]
        if mail_list:
            if args.last:
                selected_mail=mails[0]
            else:
                selected_mail = select(
                    "Select mail",
                    choices=mail_list,
                    style=style,
                    instruction=" "
                ).ask()
            MailTools.read_mail(selected_mail)
        else:
            print("No mails.")

    def wait(self):
        """ Listen for new messages on specified mailbox """
        selected_mailbox = MailTools.find_mailbox(args.address,self.box)
        print(f"Waiting new mails for {selected_mailbox.address}")
        mails=selected_mailbox.get_mail_list()
        if mails:
            print(f"Last mail was: {mails[0]}")
        print("Press Ctrl+C to Abort.",end="\r")
        count = cur_count = len(mails)
        while count == cur_count:
            try:
                mails=selected_mailbox.get_mail_list()
                cur_count = len(mails)
            except (KeyboardInterrupt,TypeError):
                PrtTools.clear_line()
                print('Aborted.')
                sys.exit()
            except (ConnectionError, Timeout, ConnectTimeout):
                pass
        PrtTools.clear_line()
        MailTools.read_mail(mails[0])
