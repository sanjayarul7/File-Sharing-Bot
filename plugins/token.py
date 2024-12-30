from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from database.database import generate_token, verify_token, revoke_token, get_user_tokens
from config import ADMINS

@Bot.on_message(filters.command("gentoken") & filters.private & filters.user(ADMINS))
async def generate_token_command(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: /gentoken <user_id>")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("Invalid user ID.")

    token = await generate_token(user_id)
    await message.reply_text(f"Generated token for user {user_id}:\n`{token}`")

@Bot.on_message(filters.command("verifytoken") & filters.private & filters.user(ADMINS))
async def verify_token_command(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: /verifytoken <token>")
    token = message.command[1]
    user_id = await verify_token(token)
    if user_id:
        await message.reply_text(f"Token is valid for user: {user_id}")
    else:
        await message.reply_text("Invalid token.")

@Bot.on_message(filters.command("revoketoken") & filters.private & filters.user(ADMINS))
async def revoke_token_command(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: /revoketoken <token>")
    token = message.command[1]
    await revoke_token(token)
    await message.reply_text("Token revoked.")

@Bot.on_message(filters.command("gettokens") & filters.private & filters.user(ADMINS))
async def get_tokens_command(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: /gettokens <user_id>")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("Invalid user ID.")
    tokens = await get_user_tokens(user_id)
    if tokens:
        token_list = "\n".join([f"`{token}`" for token in tokens])
        await message.reply_text(f"Tokens for user {user_id}:\n{token_list}")
    else:
        await message.reply_text(f"No tokens found for user {user_id}.")
