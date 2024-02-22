import os
import telebot
from datetime import datetime
import string
import random
from multicolorcaptcha import CaptchaGenerator

now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

BOT_TOKEN = "6233112256:AAGQdcEu-o8e3rO3GavKENL4K2_-O5JRtcw"

bot = telebot.TeleBot(BOT_TOKEN)


def randomstring(length):
  return ''.join(
    random.choices(string.ascii_uppercase + string.digits, k=length))


def send_reply(message, text):
  bot.reply_to(message, f"{text}", parse_mode='MarkdownV2')


def send_message(messageid, text):
  bot.send_message(messageid, f"{text}", parse_mode='MarkdownV2')


@bot.message_handler(commands=['start'])
def send_welcome(message):
  teleuser = message.from_user.username
  print(f"> bot started for {teleuser} [{dt_string}]")
  bot.send_photo(message.chat.id,
                 photo=open('images/welcome_banner.jpg', 'rb'))
  send_message(
    message.chat.id,
    "To login run: /login user pass\n\nTo register run: /register user pass repass"
  )


@bot.message_handler(commands=['login'])
def send_login(message):
  teleuser = message.from_user.username
  if "/login " in message.text:
    msg = (message.text).replace("/login ", "")
    data = msg.split(" ")
    if len(data) == 2:
      global username, password
      username, password = msg.split(" ")
      print(f"> login for {teleuser} > {username}:{password} [{dt_string}]")
      bot.send_photo(message.chat.id,
                     photo=open('images/verify_banner.jpg', 'rb'))
      send_message(message.chat.id, "To verify run: /lverify answer")
      CAPCTHA_SIZE_NUM = 2
      generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)
      captcha = generator.gen_captcha_image(difficult_level=3)
      math_captcha = generator.gen_math_captcha_image(difficult_level=2,
                                                      multicolor=True)
      image = captcha.image
      characters = captcha.characters
      global math_equation_result, math_equation_string
      math_image = math_captcha.image
      math_equation_string = math_captcha.equation_str
      math_equation_result = math_captcha.equation_result
      image.save("CAPTCHA.png", "png")
      math_image.save("CAPTCHA.png", "png")
      print(
        f"> generate captcha ({math_equation_string})({math_equation_result}) for user {teleuser} [{dt_string}]"
      )
      bot.send_photo(message.chat.id, photo=open('CAPTCHA.png', 'rb'))
    else:
      send_reply(message, f"Not enough args")
  else:
    send_reply(message, f"No args given")


@bot.message_handler(commands=['register'])
def send_register(message):
  teleuser = message.from_user.username
  if "/register " in message.text:
    msg = (message.text).replace("/register ", "")
    data = msg.split(" ")
    if len(data) == 3:
      global username, password
      username, password, repassword = msg.split(" ")
      print(
        f"> register for {teleuser} > {username}:{password}:{repassword} [{dt_string}]"
      )
      if password == repassword:
        bot.send_photo(message.chat.id, photo=open('verify_banner.jpg', 'rb'))
        send_message(message.chat.id, "To verify run: /rverify answer")

        # Captcha image size number (2 -> 640x360)
        CAPCTHA_SIZE_NUM = 2

        # Create Captcha Generator object of specified size
        generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)

        # Generate a captcha image
        captcha = generator.gen_captcha_image(difficult_level=3)
        math_captcha = generator.gen_math_captcha_image(difficult_level=2,
                                                        multicolor=True)

        # Get information of standard captcha
        image = captcha.image
        characters = captcha.characters

        # Get information of math captcha
        global math_equation_result, math_equation_string
        math_image = math_captcha.image
        math_equation_string = math_captcha.equation_str
        math_equation_result = math_captcha.equation_result

        # Save the images to files
        image.save("CAPTCHA.png", "png")
        math_image.save("CAPTCHA.png", "png")

        print(
          f"> generate captcha ({math_equation_string})({math_equation_result}) for user {teleuser} [{dt_string}]"
        )

        bot.send_photo(message.chat.id, photo=open('CAPTCHA.png', 'rb'))
      else:
        send_reply(message, f"Passwords do not match")
    else:
      send_reply(message, f"Not enough args")
  else:
    send_reply(message, f"No args given")


@bot.message_handler(commands=['lverify'])
def send_lverify(message):
  teleuser = message.from_user.username
  if math_equation_result:
    if math_equation_result in (message.text).replace("/lverify ", ""):
      print(
        f"> captcha solved successfully ({math_equation_string})({math_equation_result}) by user {teleuser} [{dt_string}]"
      )
      send_reply(message, f'*Solved successfully*')
      authlist = open("logins").read().splitlines()
      if f"{username}:{password}" in authlist:
        send_message(message.chat.id, f"*Logged in as, {username}*")
      else:
        send_message(message.chat.id, f"*Invalid Credentals, {username}*")
    else:
      send_reply(message, f'Incorrect Attempt')


@bot.message_handler(commands=['rverify'])
def send_rverify(message):
  teleuser = message.from_user.username
  if math_equation_result:
    if math_equation_result in (message.text).replace("/rverify ", ""):
      print(
        f"> captcha solved successfully ({math_equation_string})({math_equation_result}) by user {teleuser} [{dt_string}]"
      )
      send_reply(message, f'Solved successfully')
      authlist = open("logins").read().splitlines()
      if f"{username}:{password}" in authlist:
        send_reply(message, f'*Account Exists*')
      else:
        for account in authlist:
          accusername, accpassword = account.split(":")
          if accusername == username:
            send_reply(message, f'*Username Taken*')
          else:
            with open("logins", "a") as logins:
              logins.write("\n")
              logins.write(f"{username}:{password}")
      send_message(
        message.chat.id,
        f"*Registered {username}*\n\nNow you can login with /login user pass")
    else:
      send_reply(message, f'Incorrect Attempt')


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
  bot.reply_to(message, message.text)


print(f"> Telegram Bot Started [{dt_string}]")


def run_bot():
  bot.infinity_polling()
