import douyin_utils
import os
import discord

promoted_channel_id = douyin_utils.promoted_channel_id
headers = douyin_utils.headers
monitoring_channel_ids = douyin_utils.monitoring_channel_ids
promoting_index = douyin_utils.promoting_index

async def promote_douyin_video(reacted_channel, reacted_message, client, TagPromoter=""):
  history_messages = await reacted_channel.history(limit=200).flatten()
  for msg in history_messages:
    if msg.id == reacted_message.id:
      index = history_messages.index(msg)
      index += 1
  info_message = history_messages[index]
  promoted_channel = client.get_channel(promoted_channel_id)
  if(TagPromoter==""):
    promoter_message = "\n`该视频由txxx被晋升t0！`评选：后门系统"
    await promoted_channel.send(info_message.content+promoter_message)
  else:
    promoter_message = "\n`该视频由txxx被晋升t0！`评选："
    await promoted_channel.send(info_message.content+promoter_message+TagPromoter)
  douyin_utils.download_video(reacted_message.attachments[0].url,headers)
  await promoted_channel.send(file=discord.File('video.mp4'))
  if os.path.exists("video.mp4"):
    os.remove("video.mp4")
  else:
    print("出现错误！") 
  deleting_message = await reacted_channel.fetch_message(info_message.id)
  await deleting_message.delete()
  await reacted_message.delete()

async def on_raw_reaction_add(payload, client):
  channel_id = payload.channel_id
  reacted_channel = client.get_channel(channel_id)
  message_id = payload.message_id
  reacted_message = await reacted_channel.fetch_message(message_id)

  if str(channel_id) in monitoring_channel_ids:
    if str(payload.emoji) == "❤️":
      for reaction in reacted_message.reactions:
        if str(reaction.emoji) == "❤️":
          if reaction.count > promoting_index:
            promoters = await reaction.users().flatten()
            TagPromoter = ""
            for promoter in promoters:
              if not promoter.id == 821773793176453120:
                TagPromoter = TagPromoter + "<@" + str(promoter.id) + "> " 
            await promote_douyin_video(reacted_channel, reacted_message, client, TagPromoter)