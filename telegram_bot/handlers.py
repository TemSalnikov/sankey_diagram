from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery 
import utils

import kb
import text

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.main_menu)

@router.callback_query(F.data == "main_menu")
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.main_menu, reply_markup=kb.main_menu)

@router.callback_query(F.data == "generate_diagram")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.bank_menu, reply_markup=kb.bank_menu)
    # await state.set_state(Gen.text_prompt)
    # await clbck.message.edit_text(text.bank_menu)
    

# async def menu(msg: Message):
#     await msg.answer(text.bank_menu, reply_markup=kb.bank_menu)

# @router.callback_query(F.data == "load_vtb")
# async def menu(msg: Message):
#     await msg.answer(text.load_vtb)
@router.callback_query(F.data == "load_vtb")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.load_vtb, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "load_sber")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.load_sber, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "load_y")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.load_y, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "load_t")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.load_t, reply_markup=kb.exit_kb)

# @router.callback_query(F.data == "load_sber")
# async def menu(msg: Message):
#     await msg.answer(text.load_sber)

# @router.callback_query(F.data == "load_y")
# async def menu(msg: Message):
#     await msg.answer(text.load_y)

# @router.callback_query(F.data == "load_t")
# async def menu(msg: Message):
#     await msg.answer(text.load_t)


# @router.callback_query(F.data == "generate_text")
# async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
#     await state.set_state(Gen.text_prompt)
#     await clbck.message.edit_text(text.gen_text)
#     await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)

# @router.message(Gen.text_prompt)
# @flags.chat_action("typing")
# async def generate_text(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     res = await utils.generate_text(prompt)
#     if not res:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)

# @router.callback_query(F.data == "generate_image")
# async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
#     await state.set_state(Gen.img_prompt)
#     await clbck.message.edit_text(text.gen_image)
#     await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)

# @router.message(Gen.img_prompt)
# @flags.chat_action("upload_photo")
# async def generate_image(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     img_res = await utils.generate_image(prompt)
#     if len(img_res) == 0:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.delete()
#     await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)