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

class Config:
    HOST = "https://m.kuku.lu"
    PATH_ADDRESS_LIST = "/index._addrlist.php"
    PATH_SNED_MAIL = "/new.php"
    PATH_RECV_MAIL = "/recv.php"
    PATH_MAIL_LIST = "/recv._ajax.php"
    PATH_MAIL_CONTENT = "/smphone.app.recv.view.php"

    HEADERS: dict = {}

    SESSION_ID_KEY = "cookie_uidenc_seted"
    CSRF_TOKEN_KEY = "cookie_csrf_token"
    CSRF_TOKEN_TAG = "cookie_csrf_token"

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