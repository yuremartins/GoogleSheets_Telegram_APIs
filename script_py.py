# -*- coding: utf-8 -*-
"""script.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MYfKCaz4SQfK3pa9VzB4ruUzf8XGzHMN
"""

pip install pyTelegramBotAPI

import telebot
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Definindo as credenciais do bot do Telegram e das APIs do Google Sheets
telegram_token = 'BOT_TOKEN'
google_credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', ['https://www.googleapis.com/auth/spreadsheets'])
google_sheets_id = 'ID_SHEETS'

# Definindo a função para lidar com as mensagens de adição de itens ao estoque
def handle_message(message): 
    chat_id = message.chat.id
    text = message.text
    # Separando a mensagem em uma lista de itens
    items = text.split(',') 
    
    items = message.text.split('/')
    if len(items) < 3:
        bot.reply_to(message, 'Por favor, forneça uma mensagem no formato "item/quantidade/preço".')
        return

    # Obter a data atual
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")

    # Extrair os valores do item, quantidade e preço da mensagem
    description = items[0]
    quantity = items[1]
    value = items[2]

try:
        service = build('sheets', 'v4', credentials=google_credentials)
        sheet = service.spreadsheets()

        # Criar uma lista com os valores do item, quantidade, preço e data atual
        row = [current_time, description, quantity, value]

        # Inserir a lista de valores na planilha na primeira linha
        result = sheet.values().append(
            spreadsheetId=google_sheets_id,
            range='Sheet1!A1',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()

        bot.send_message(chat_id, 'Mensagem salva com sucesso!')
    except HttpError as error:
        bot.send_message(chat_id, f'Ocorreu um erro ao salvar a mensagem: {error}')

# Iniciar o bot com o token
bot = telebot.TeleBot(telegram_token) 

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    handle_message(message)

bot.polling()