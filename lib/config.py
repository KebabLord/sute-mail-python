from questionary import Style as PromptStyle

class Files:
    """ Path to files """
    mailboxes=".mails"
    ses_token=".ses"
    burner_accounts=".accs"

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
