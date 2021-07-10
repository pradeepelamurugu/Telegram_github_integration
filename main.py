import telebot
from github import Github
import requests
from telebot import types
API_KEY = 'YOUR BOT API KEY '
global repo_name
global file_name
token = "YOUR_GITHUB_TOKEN"

g = Github(token)


user = g.get_user()

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['hi'])
def greet(message):
    bot.reply_to(message, "hey, hi "+message.from_user.first_name+"!")


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Your companian.
""")
    
@bot.message_handler(commands=['create_file'])
def send_welcome(message):
    
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for repo in g.get_user().get_repos():
      print(repo)
      markup.add(types.KeyboardButton(str(repo)[39:len(str(repo))-2]))
    msg = bot.reply_to(message, 'Select Repositories', reply_markup=markup)
    
    
    print(msg)
    bot.register_next_step_handler(msg, get_repo)
    


def get_repo(message):
    try:
        global repo_name
        repo_name = message.text
        msg = bot.reply_to(message,"file_name?")
        bot.register_next_step_handler(msg, get_file_name)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def get_file_name(message):
    try:
        global file_name
        file_name = message.text
        msg = bot.reply_to(message,"code?")
        bot.register_next_step_handler(msg, creation_process)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def creation_process(message):
    user = g.get_user()
    repo = user.get_repo(repo_name)
    repo.create_file(path=file_name,message="created by bot",content=message.text,branch="main")
    bot.reply_to(message,"File created successfully!!")

bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()


bot.polling()