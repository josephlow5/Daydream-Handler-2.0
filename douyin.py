import discord
import os
import requests
import re
import douyin_utils

headers = douyin_utils.headers
monitoring_channel_ids = douyin_utils.monitoring_channel_ids

def get_douyin_info(url):
  with open("douyin_parse.txt",encoding='utf-8') as logFile:
    logs = logFile.readlines()
  LoggedContent = ""
  for log in logs:
    if "|||URL_SEPERATOR|||" in log:
      log_url = log.split("|||URL_SEPERATOR|||")[0]
      log_content = log.split("|||URL_SEPERATOR|||")[1]
      if url == log_url:
        if "Video Not Found!" not in log:
          LoggedContent = log_content
  if LoggedContent != "":
    return LoggedContent.split("|||||")
      
  Retry = 3
  while True:
    try:
      douyin_id = douyin_utils.get_douyin_id(url)
      douyin_info = douyin_utils.get_douyin_parsed_info(douyin_id)
      #response = requests.get(douyinapilink+url, timeout=15, headers=headers)  #Deprecated since we parse on local now
      break
    except:
      Retry -= 1
      if Retry < 0:
        break
      continue
  try:
    if("||||||||||||||||||||" in douyin_info):
      return []
    else:
      with open("douyin_parse.txt","a",encoding='utf-8') as logFile:
        logFile.write(url+"|||URL_SEPERATOR|||"+douyin_info+"\n")
      return douyin_info.split("|||||")
  except:
    return []


def process_text_content(directURL,targetwebsite,authorID,authorName,Description,LikeCount,Thumbnail,Duration,message):
  video_info = "**---------------------------------\n作者："+authorName+" ("+authorID+")"+"\n---------------------------------**\n*"+Description+"*\n"+ "> 抖音分享地址：<"+targetwebsite+ ">\n> 平台分享地址：<[befamous_link]>\n> 共"+LikeCount+"次按赞"+"，多谢分享！谢谢"+message.author.mention
  if len(message.mentions)>0:
    video_info += "\n`特别推荐给：`"
    for mentioned in message.mentions:
      video_info += mentioned.mention + " "
  if "|ImageSep|" in directURL:
    video_info = video_info.replace("\n> 平台分享地址：<[befamous_link]>","")
  return video_info
  
async def process_visual_content(directURL,video_info,message,Thumbnail,Description,Duration):
  if "|ImageSep|" in directURL:
    await message.channel.send(video_info)
    douyin_utils.download_images(directURL,headers)
    for image in directURL.split("|ImageSep|"):
      filename = 'image{}.jpg'.format(directURL.split("|ImageSep|").index(image))
      await message.channel.send(file=discord.File(filename))
      if os.path.exists(filename):
        try:
          os.remove(filename)
        except:
          pass
  else:
    upload = douyin_utils.upload_befamous_cyou(directURL,Thumbnail,Description,video_info,Duration,headers)
    if not "Error! " in upload:
      video_info = video_info.replace("[befamous_link]",upload)
    else:
      video_info = video_info.replace("\n> 平台分享地址：<[befamous_link]>","")
    await message.channel.send(video_info)
    if os.path.exists("video.mp4"):
      try:
        video_message = await message.channel.send(file=discord.File('video.mp4'))
        if str(video_message.channel.id) in monitoring_channel_ids:
          await video_message.add_reaction("❤️")
      except:
        await message.channel.send("**这视频太大了,在DC无法发送...还是去我们平台看吧~**")
      try:
        os.remove("video.mp4")
      except:
        pass
    

async def on_message(message,client):
  if "https://v.douyin.com/" in message.content:
    targetwebsite = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
    reply = await message.channel.send(message.author.mention+" 感谢你的分享，马上开始处理这个视频!")

    douyin_info = get_douyin_info(targetwebsite)
    if len(douyin_info) > 6:
      directURL = douyin_info[0]
      authorID = douyin_info[1]
      authorName = douyin_info[2]
      Description = douyin_info[3]
      LikeCount = douyin_info[4]
      Thumbnail = douyin_info[5]
      Duration = douyin_info[6]

      i = process_text_content(directURL,targetwebsite,authorID,authorName,Description,LikeCount,Thumbnail,Duration,message)
      await process_visual_content(directURL,i,message,Thumbnail,Description,Duration)
    else:
      await message.channel.send("非常抱歉，我找不到这个视频的资讯，默哀3秒钟 <"+targetwebsite+">", delete_after=10)
      
    await message.delete()
    await reply.delete()

