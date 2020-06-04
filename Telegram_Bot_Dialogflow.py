# Library
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token=token_telegram) # Telegram API Token
dispatcher = updater.dispatcher

# Commands
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Olá, sobre o que você gostaria de conversar?')

# Text
def textMessage(bot, update):
    request = apiai.ApiAI(token_apiai).text_request() # Dialogflow API Token
    request.lang = 'pt-BR' # Request language
    request.session_id = SESSION # ID dialog session (for bot training)
    request.query = update.message.text.lower() # Send request to AI ИИ with the user message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Take JSON answer
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Desculpe, não entendi...')
        
# Handlers
if __name__ == "__main__":
    
    start_command_handler = CommandHandler('start', startCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    # Add handlers to the dispatcher
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Start update search
    updater.start_polling(clean=True)
    # Stops the bot
    updater.idle()
