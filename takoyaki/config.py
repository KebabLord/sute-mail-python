from os import path,name,mkdir
from questionary import Style as PromptStyle

def get_base():
    """ Return software's basedirectory to log data"""
    homedir=path.expanduser('~')
    if name=="nt":
        base=path.join(homedir,"Takoyaki")
    else:
        base=path.join(homedir,".config","takoyaki")
    if not path.isdir(base):
        mkdir(base)
    return base

class Files:
    """ Path to files """
    base=get_base()
    mailboxes=path.join(base,"mails")
    ses_token=path.join(base,"token")
    burner_accounts=path.join(base,"accounts")

style = PromptStyle([
    ('qmark', 'fg:#5F819D bold'),
    ('question', 'fg:#07d1e8 bold'),
    ('answer', 'fg:#48b5b5 bg:#hidden bold'),
    ('pointer', 'fg:#48b5b5 bold'),
    ('highlighted', 'fg:#07d1e8'),
    ('selected', 'fg:#48b5b5 bg:black bold'),
    ('separator', 'fg:#6C6C6C'),
    ('instruction', 'fg:#77a371'),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])
