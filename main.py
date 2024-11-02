import telebot 
from config import token
from logic import Pokemon
from datetime import datetime

bot = telebot.TeleBot(token) 


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    try:
        bot.reply_to(message, """\
Hi there, I am BibobBot.
I veryveryveryvery cool! I universal. Just tell me and I'll do it. Write "/info" and you see my skills.\
""")
    except Exception as e:
        print(f"Error in send_welcome: {e}")

@bot.message_handler(commands=['info'])
def info(message):
    try:
        username = message.from_user.username
        if username in Pokemon.pokemons.keys():
            pokemon = Pokemon.pokemons[username]
            bot.send_message(message.chat.id, pokemon.info())
        else:
            bot.reply_to(message, "У тебя еще нет покемона. Используй команду /go, чтобы создать его!")
    except Exception as e:
        print(f"Error in info: {e}")

@bot.message_handler(commands=['go'])
def go(message):
    try:
        username = message.from_user.username
        if username not in Pokemon.pokemons.keys():
            pokemon = Pokemon(username)
            Pokemon.pokemons[username] = pokemon 
            bot.send_message(message.chat.id, pokemon.info())
            bot.send_photo(message.chat.id, pokemon.show_img())
        else:
            bot.reply_to(message, "Ты уже создал себе покемона!")
    except Exception as e:
        print(f"Error in go: {e}")

@bot.message_handler(commands=['feed'])
def feed(self):
    try:
        if self.last_fed is None or datetime.now() - self.last_fed >= datetime(hours=1):  
            self.health += 20  
            if self.health > 100: 
                self.health = 100
            self.last_fed = datetime.now()  
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in feed: {e}")

bot.polling(none_stop=True)
