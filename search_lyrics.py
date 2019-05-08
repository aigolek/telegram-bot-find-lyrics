import requests
import telebot
from telebot import types
SEARCH_LYRICS_APIKEY = '63f47f572a4793611aef062eee7154b7'

bot = telebot.TeleBot("667645024:AAF9pP5mYfoNotmugsioUp1zKiK99-UWQsc") 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, "Hello " + user_name + "! Type any song's title to find out its lyrics")

@bot.message_handler(content_types=['text'])
def send_lyrics(message):
    chat_id=message.chat.id
    song_title = message.text.lower()
    SEARCH_LYRICS_URL = "http://api.musixmatch.com/ws/1.1/track.search?apikey=" + SEARCH_LYRICS_APIKEY + "&page_size=3&page=1&s_track_rating=desc&q_track=" + song_title
    if song_title:
        res = requests.get(SEARCH_LYRICS_URL) 
        if res.status_code == 200:
            tracks = res.json()['message']['body']['track_list']
            if len(tracks) == 0:
                bot.send_message(chat_id, "Hmm... No songs with such title found..." + u'\U0001F62D') 
            else:            
                if len(tracks) > 1:
                    bot.send_message(chat_id, "Hmm... Looks like there are several tracks with such title..." ) 
                keyboard = types.InlineKeyboardMarkup()
                for track in tracks:
                    track_id = track['track']['track_id']
                    artist_name = track['track']['artist_name']
                    btn=types.InlineKeyboardButton(artist_name, callback_data=track_id)
                    keyboard.add(btn)  
                bot.send_message(chat_id, "Please choose the artist of the song:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handleInlineButton(call):
    chat_id=call.message.chat.id
    if call.message:
        LYRICS_URL = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey="+SEARCH_LYRICS_APIKEY+"&track_id="+call.data
        res = requests.get(LYRICS_URL) 
        if res.status_code == 200:    
            print(res.json())
            if len(res.json()['message']['body']) == 0:
                bot.send_message(chat_id, "Hmm... No lyrics found...¯\_(ツ)_/¯" ) 
            else:        
                lyrics = res.json()['message']['body']['lyrics']['lyrics_body']
                bot.send_message(chat_id, res.json()['message']['body']['lyrics']['lyrics_body'])  

bot.polling()    

