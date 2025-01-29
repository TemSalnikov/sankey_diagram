from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
main_menu = [
    [InlineKeyboardButton(text="📝 Сформировать Sankey-диаграму", callback_data="generate_diagram")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]
bank_menu = [
    [InlineKeyboardButton(text="🏦 ВТБ", callback_data="load_vtb"),
    InlineKeyboardButton(text="🏦 Сбер", callback_data="load_sber")],
    [InlineKeyboardButton(text="🏦 Yandex", callback_data="load_y"),
    InlineKeyboardButton(text="🏦 Т-банк", callback_data="load_t")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu"),
    InlineKeyboardButton(text="🔎 Помощь", callback_data="help")],
    [InlineKeyboardButton(text="✅ Готово", callback_data="complete")]
]
main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu)
bank_menu = InlineKeyboardMarkup(inline_keyboard=bank_menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]])