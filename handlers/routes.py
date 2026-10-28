from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot
import asyncio
# import aiosqlite
# from aiogram.types import FSInputFile
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram import Bot 

router = Router()

subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "Your standard message")
                except Exception:
                    pass

        await asyncio.sleep(10)    

@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        "Hi!\n"
        "I can help with share!\n\n"
        "Commands:\n"
        "/subscribe - subscibe to notifications\n"
        "/unsubscribe - unsubscribe\n"
        "/subscribers - list of subscribers"
    )

@router.message(Command('subscribe'))
async def subscibe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)

    await message.answer("You subscribed!")


@router.message(Command('unsubscribe'))
async def unsubscibe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)

    await message.answer("You unsubscribed!")

@router.message(Command('subscribers'))
async def subscibers_cmd(message: Message):
    if not subscribers:
        await message.answer("There is no one yet")
        return


    text = "Subscribers:\n"
    for uid in subscribers:
        text += f"{uid}\n"    
    await message.answer(text)


# -- #7

# DB_NAME = "bot.sql"

# async def init_db():
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY, 
#                         full_name TEXT,
#                         age INTEGER
#                         )
#                         """)

#         await db.commit()                

# async def add_user(full_name, age):
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("INSERT INTO users(full_name, age) VALUES(?, ?)", (full_name, age))
#         await db.commit() 

# async def get_users():
#     async with aiosqlite.connect(DB_NAME) as db:
#         cursor = await db.execute("SELECT full_name, age FROM users")
#         result = await cursor.fetchall()         
#         return result  

# # ---

# @router.message(Command("start"))
# async def start(message: Message):
#     await init_db()
#     await message.answer("Hi!\nWrite command: /reg AGE")


# @router.message(Command("reg"))
# async def reg(message: Message):
#     parts = message.text.strip().split()

#     if len(parts) != 2 or not parts[1].isdigit():
#         await message.answer("Write the command correct!")
#         return

#     await add_user(message.from_user.full_name, int(parts[1]))

#     await message.answer("Ready!")

# @router.message(Command("users"))
# async def users(message: Message):
#     users = await get_users()

#     if not users:
#         await message.answer("There is no users in DataBase!")
#         return

#     text = "Users in Base:\n\n"
#     for full_name, age in users: 
#         text += f"- {full_name} - <code>{age}</code>\n"

#     await message.answer(text, parse_mode="HTML")

# @router.message(Command("start"))
# async def start(message: Message):
#     await message.answer(
#         "Hi! I am ordinary shop bot!.\nWrite a command: /product ID\n\nInstance:" `<b>/product 1</b>`,
#         parse_mode="HTML"
#     )

# ---

# import aiohttp

# async def get_product(product_id):
#     url = f"https://fakestoreapi.com/products/{product_id}"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             if resp.status == 404:
#                 return None 

#             data = await resp.json()
#             return data     

# ---

# class Form(StatesGroup):
#     name = State()
#     age = State()
#     email = State()
# @router.message(Command("product"))
# async def get_product_cmd(message: Message):
#     parts = message.text.strip().split()
#     # products 23 some - example
#     if len(parts) != 2:
#         await message.answer("Use: /product 1")
#         return

#     product_id = parts[1]
#     if not product_id.isdigit():
#         await message.answer("The ID of product must be number")
#         return

#     await message.answer(f"Seeking product with ID: {product_id}")


#     try: 
#         product = await get_product(int(product_id))
#     except Exception:
#         await message.answer("Can't connect with server :(")
#         return

#     if product is None:
#         await message.answer("Sorry, This product is not available")
#         return     

#     title = product.get("title", "No name")
#     price = product.get("price", "-")
#     desc = product.get("description", "No description")
#     category = product.get("category", "No category")
#     image = product.get("image")

#     text = (
#         f"<b>{title}</b>\n\n"
#         f"Category: <i>{category}</i>\n"
#         f"Price: <b>{price}</b>\n"
#         f"{desc}"
#     )

#     photo = FSInputFile("no-image.png")
#     await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")

# if image: 
#     await message.answer_photo(photo=image, caption=text, parse_mode="HTML")
# else:    
#     await message.answer(text, parse_mode="HTML")

# await state.set_state(Form.name)
# await message.answer("Let's begin to fill the form!\nFirstly, write your name:")

# @router.message(Command("cancel"))
# async def cancel_form(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Form canceled!")

# @router.message(Form.name, F.text)
# async def process_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Good!\nNow write your age:")
#     await state.set_state(Form.age)

# @router.message(Form.name)
# async def process_name_invalid(message: Message):
#     await message.answer("Please send text for your name!")

# @router.message(Form.age, F.text)
# async def process_age(message: Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer("Age must be a number!")
#         return 

#     age = int(message.text)

#     if age < 1 or age > 100:
#         await message.answer("Age must be from 1 to 100")
#         return  

#     await state.update_data(age=age)
#     await message.answer("Great!\nNow write your email:")
#     await state.set_state(Form.email)

# @router.message(Form.age)
# async def process_age_invalid(message: Message):
#     await message.answer("Please send a valid number for your age!")

# @router.message(Form.email, F.text)
# async def process_email(message: Message, state: FSMContext):
#     email_text = message.text

#     if "@" not in email_text or "." not in email_text:
#         await message.answer("Email must contain '@' and '.'!")
#         return

#     await state.update_data(email=email_text)

#     data = await state.get_data()
#     name = data.get("name")
#     age = data.get("age")
#     email = data.get("email")
    
#     await message.answer(f"Perfect!\nThe form is ready!\n\nName: {name}\nAge: {age}\nEmail: {email}")
#     await state.clear()

# @router.message(Form.email)
# async def process_email_invalid(message: Message):
#     await message.answer("Please send text for your email!")

# @router.message(F.photo)
# async def process_photo(message: Message):
#     photo = message.photo[-1]
#     file_id = photo.file_id

#     await message.answer(
#         f"You have send the photo!\nID photo: <code>{file_id}</code>",
#         parse_mode="HTML"
#     )

#     await message.answer_photo(file_id, caption="this is your photo")

# @router.message(F.video)
# async def process_photo(message: Message):
#     video = message.video
#     file_id = video.file_id
#     duration = video.duration

#     await message.answer(
#         f"You have send the video!\nID video: <code>{file_id}</code>\nDuration: <code>{duration}</code>",
#         parse_mode="HTML"
#     )

#     await message.answer_video(file_id, caption="this is your video")    

# @router.message(F.animation)
# async def proccess_animation(message: Message):
#     animation = message.animation

#     await message.answer(
#         f"Вы отправили animation!\nID animation: <code>{animation.file_id}</code>",
#         parse_mode="HTML"
#     )

#     await message.answer_animation(animation.file_id, caption="Вот ваше animation")


# @router.message(F.document)
# async def proccess_document(message: Message, bot: Bot):
#     document = message.document
#     file_id = document.file_id

#     file = await bot.get_file(file_id)  
#     file_path = file.file_path
    
#     local_path = f'Downloads/{document.file_name}' 

#     await bot.download_file(file_path=file_path, destination=local_path)

#     await message.answer('File Saved!')

# @router.message(Command("file"))
# async def send_file(message: Message):    
#     file = FSInputFile('files/example.txt')

#     await message.answer_document(file)