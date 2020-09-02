# Fully Written by @HeisenbergTheDanger (Keep credits else gay)
# Permission Seeked By @StarkXD - Approved

import asyncio
import datetime
from telethon import events

from var import Var
from uniborg.util import admin_cmd, sudo_cmd, edit_or_reply
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputMediaUploadedDocument,
    InputMediaUploadedPhoto,
    InputPeerNotifySettings,
    InputStickerSetID,
    InputStickerSetShortName,
    MessageMediaPhoto
)
from userbot.plugins.sql_helper.broadcast_sql import in_channels, add_channel, rm_channel, get_all_channels

logs_id = Var.PRIVATE_GROUP_ID



@borg.on(admin_cmd("bforward ?(.*)"))
@borg.on(sudo_cmd("bforward ?(.*)", allow_sudo=True))
async def forw(event): 
  if event.fwd_from:
    return
  if not event.is_reply:
    await edit_or_reply("Reply to a message to broadcast.")
    return
  channels = get_all_channels()
  await edit_or_reply("Sending...")
  error_count = 0
  sent_count = 0 
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    message = previous_message.message
    raw_text = previous_message.raw_text
  error_count = 0
  for channel in channels:
    try:
      await borg.forward_messages(int(channel.chat_id), previous_message)
      sent_count += 1
      await edit_or_reply(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
    except Exception as error:
      try:
        await borg.send_message(logs_id, f"Error in sending at {channel.chat_id}.")
        await borg.send_message(logs_id, "Error! " + str(error))
        if error == "The message cannot be empty unless a file is provided":
            edit_or_reply("For sending files, upload in Saved Messages and reply .forward to in.")
            return
      except:
        pass
      error_count+=1
      await edit_or_reply(f"Sent : {sent_count}\nError : {error_count}")
  await edit_or_reply(f"{sent_count} messages sent with {error_count} errors.")
  if error_count > 0:
    try:
        await borg.send_message(logs_id, f"{error_count} Errors")
    except:
        await edit_or_reply("Set up log channel for checking errors.")
    
    
@borg.on(admin_cmd("broadcast ?(.*)"))
@borg.on(sudo_cmd("broadcast ?(.*)", allow_sudo=True))
async def _(event):
  if event.fwd_from:
        return
  if not event.is_reply:
    await edit_or_reply("Reply to a message to broadcast.")
    return
  channels = get_all_channels()
  error_count = 0
  sent_count = 0
  await edit_or_reply("Sending....")
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    if previous_message.sticker or previous_message.poll:
        await edit_or_reply("Reply .forward for stickers and polls.")
        return
    if previous_message.gif or previous_message.audio or previous_message.voice or previous_message.video or previous_message.video_note or previous_message.contact or previous_message.game or previous_message.geo or previous_message.invoice:     # Written by @HeisenbergTheDanger
        await edit_or_reply("Not supported. Try .forward")
        return
    if not previous_message.web_preview and previous_message.photo:
      file = await borg.download_file(previous_message.media)
      uploaded_doc = await borg.upload_file(file, file_name="img.png")
      raw_text = previous_message.text
      for channel in channels:
        try:
            if previous_message.photo:
                await borg.send_file(
                                int(channel.chat_id),
                                InputMediaUploadedPhoto(
                                    file=uploaded_doc
                                ),
                                force_document=False,
                                caption = raw_text,
                                link_preview = False
                            )
        
            sent_count += 1
            await edit_or_reply(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
        except Exception as error:
          try:
            await borg.send_message(logs_id, f"Error in sending at {chat_id}.")
            await borg.send_message(logs_id, "Error! " + str(error))
            if error == "The message cannot be empty unless a file is provided":
                event.edit("For sending files, upload in Saved Messages and reply .forward to in.")
                return
          except:
            pass
          error_count += 1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
      await edit_or_reply(f"{sent_count} messages sent with {error_count} errors.")
      if error_count > 0:
        try:
            await borg.send_message(logs_id, f"{error_count} Errors")
        except:
            pass      
    else:
      raw_text = previous_message.text
      for channel in channels:
        try:
          await borg.send_message(int(channel.chat_id), raw_text, link_preview = False)
          sent_count += 1
          await edit_or_reply(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
        except Exception as error:
          try:
            await borg.send_message(logs_id, f"Error in sending at {channel.chat_id}.")
            await borg.send_message(logs_id, "Error! " + str(error))
            if error == "The message cannot be empty unless a file is provided":
                edit_or_reply("For sending files, upload in Saved Messages and reply .forward to in.")
                return
          except:
            pass
          error_count+=1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
      await edit_or_reply(f"{sent_count} messages sent with {error_count} errors.")
      if error_count > 0:
        try:
            await borg.send_message(logs_id, f"{error_count} Errors")
        except:
            await edit_or_reply("Set up log channel for checking errors.")

# Written by @HeisenbergTheDanger

@borg.on(admin_cmd("badd ?(.*)"))
@borg.on(sudo_cmd("badd ?(.*)", allow_sudo=True))
async def add_ch(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        await event.edit("Adding...")
        previous_message = await event.get_reply_message()
        raw_text = previous_message.text
        lines = raw_text.split("\n")
        length = len(lines)
        for line_number in range(1, length - 2):
            channel_id = lines[line_number][4:-1]
            if not in_channels(channel_id):
                add_channel(channel_id)
        await event.edit("Channels added!")
        await asyncio.sleep(3)
        await event.delete()
        return
    chat_id = event.chat_id
    try:
        if int(chat_id) == logs_id:
            return
    except:
        pass
    if not in_channels(chat_id):
        add_channel(chat_id)
        await event.edit("`Added Successfuly To List`")
        await asyncio.sleep(3)
        await event.delete()
    elif in_channels(chat_id):
        await event.edit("`Channel is already is database!`")
        await asyncio.sleep(3)
        await event.delete()


@borg.on(admin_cmd("brm ?(.*)"))
@borg.on(sudo_cmd("brm ?(.*)", allow_sudo=True))
async def remove_ch(event):
    if event.fwd_from:
        return
    chat_id = event.pattern_match.group(1)
    if chat_id == "all":
        await edit_or_reply("Removing...")
        channels = get_all_channels()
        for channel in channels:
            rm_channel(channel.chat_id)
        await edit_or_reply("Database cleared.")
        return
        
    if in_channels(chat_id):
        rm_channel(chat_id)
        await edit_or_reply("Removed from database")
        await asyncio.sleep(3)
        await event.delete()
    elif in_channels(event.chat_id):
        rm_channel(event.chat_id)
        await edit_or_reply("Removed from database")
        await asyncio.sleep(3)
        await event.delete()
    elif not in_channels(event.chat_id):
        await edit_or_reply("Channel is already removed from database. ")
        await asyncio.sleep(3)
        await event.delete()
        
@borg.on(admin_cmd("listchannels"))
@borg.on(sudo_cmd("listchannels", allow_sudo=True))
async def list(event):
    if event.fwd_from:
        return
    channels = get_all_channels()
    msg = "Channels in database:\n"
    for channel in channels:
        msg += f"=> `{channel.chat_id}`\n"
    msg += f"\nTotal {len(channels)} channels."
    if len(msg) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "channels.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Channels in database",
                reply_to=event
            )
            await event.delete()
    else:
        await edit_or_reply(msg)
