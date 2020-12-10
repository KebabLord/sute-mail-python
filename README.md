<p align="center">
  <img src="https://u.teknik.io/00UzK.svg">
</p>

Takoyaki is a simple tool to create random/burner instant mails and generate registration credentials. It's simply cli version of m.kuku.lu service and a cli frontend to sute-mail-python module.

### Usage
```λ ./takoyaki.py -h
Takoyaki is an interactive burner mail creator and controller.
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
  -w, --Wait                Start listening new mails after generate (for verification mails)
  -s, --save <NAME>         Save generated info to .accs file
```
### Examples:
```
# Create a new random instant mail address
$ ./takoyaki create
created: penanegya@mirai.re

# List existing addresses
$ ./takoyaki list
1  misukedo@via.tokyo.jp
2  kyakidokya@eay.jp
3  penanegya@mirai.re

# Let's read mails on the kyakidokya@eay.jp
./takoyaki read -a kyaki
> No mails.
# or you can also specify index of address
./takoyaki read -a 2
> No mails.

# Let's create a burner account for a gaming site,
# generate a random password and a username,
# save the credentials we generated to .accs file and wait for the verification mail.
./takoyaki gen -a1 -puws "some name"
or the long version;
./takoyaki gen --address 1 --uname --password --wait --save="some name"
=== Some Name Account ===
Mail: misukedo@via.tokyo.jp
Nick: jturlj74 
Pass: v0OEksf7.maiVdJ 

Waiting new mails for misukedo@via.tokyo.jp
Press Ctrl+C to Abort.
```

