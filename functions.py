from cryptography.fernet import Fernet
from datetime import datetime
from os import system, name
import string, random, json
from simple_term_menu import TerminalMenu


def banner(debug, host, port, key, fernetkey):
  return f"""(Flask Server) (debug:{debug}) ({datetime.now()})
├── Host - ({host})
│   └── Port - ({port})
├── Fernet Key - ({fernetkey})
│   ├── Test Encryption - ({fernetencode("Hello, Flask!",fernetkey)})
│   └── Test Decryption - ({fernetdecode(fernetencode("Hello, Flask!",fernetkey),fernetkey)})
└── Default Key - ({key})"""


def loadconfig():
  with open("config.json", "r") as jsonfile:
    jsonraw = json.loads(jsonfile.read())
    return jsonraw


def clear():
  if name == "nt":
    _ = system("cls")
  else:
    _ = system("clear")


def fernetencode(data, key):
  f = Fernet(key)
  token = f.encrypt(data.encode("utf-8"))
  return token


def fernetdecode(data, key):
  f = Fernet(key)
  return f.decrypt(data)


def getkey(length):
  return "".join(
    random.choices(string.ascii_uppercase + string.digits, k=length))


def getfernetkey():
  return Fernet.generate_key()
