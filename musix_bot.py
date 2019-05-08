import telebot
from telebot import types
import musix_service as service

API_KEY = 'xxx'
bot = telebot.TeleBot("xxx") 
musix = service.MusixService(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, "Hello " + user_name + "! Type any song's title to find out its lyrics")

@bot.message_handler(content_types=['text'])
def send_lyrics(message):
    chat_id=message.chat.id
    song_title = message.text.lower()
    artists_list = musix.search_artist_by_track(song_title)
    keyboard = types.InlineKeyboardMarkup()

    for track_tuple in artists_list:
        btn=types.InlineKeyboardButton(track_tuple[0], callback_data=track_tuple[1])
        keyboard.add(btn)  
    
    bot.send_message(chat_id, "Please choose the artist of the song:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handleInlineButton(call):
    chat_id=call.message.chat.id
    if call.message:
        lyrics_tuple = musix.get_lyrics_by_track_id(call.data)
        if lyrics_tuple[1] == None:
            bot.send_message(chat_id, "No lyrics found." ) 
        else:        
            bot.send_message(chat_id, lyrics_tuple[1])  

bot.polling()    

