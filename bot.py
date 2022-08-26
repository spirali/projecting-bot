import discord
import os

client = discord.Client()
IMAGE_DIR = None


async def save_attachment(attachment, path):
    target_name = os.path.join(path, attachment.filename)
    target_part = target_name + ".part"
    print("Saving as", target_part)
    with open(target_part, "wb") as f:
        await attachment.save(f)
    print("Renaming", target_part, "to", target_name)
    os.rename(target_part, target_name)
    print(attachment.filename, "saved")


@client.event
async def on_message_edit(before, after):
    print("On message edit", after)
    if "%" in before.content and "%" not in after.content:
        for a in after.attachments:
            await save_attachment(a, IMAGE_DIR)


@client.event
async def on_message(message):
    print("On message", message)
    for a in message.attachments:
        await save_attachment(a, IMAGE_DIR)


def start_bot(bot_key, image_dir):
    global IMAGE_DIR
    IMAGE_DIR = image_dir
    client.run(bot_key)
