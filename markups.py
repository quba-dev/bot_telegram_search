from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('🙅‍♂️ Главное меню')

# --- Главное меню --- #

btnRandom = KeyboardButton('🎲 Рандомное число игральной кости')
btnMoney = KeyboardButton('💲 Курс валют')
btnMovie = KeyboardButton('🎦 как искать КИНО')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMovie,btnRandom, btnMoney)
