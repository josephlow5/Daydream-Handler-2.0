import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
promoted_channel_id = 818896480449462322
monitoring_channel_ids = ['818897521869979748']
promoting_index = 3
upload_api = "<YOUR PLATFORM API UPLOAD LINK>"
addvideo_api = "<YOUR PLATFORM API VIDEO UPLOAD LINK>"
directory_to_replace = "<YOUR PLATFORM UPLOAD DIRECTORY>"


def get_douyin_id(douyin_url):
  headers = {
      'authority': 'v.douyin.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en-US,en;q=0.9',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  }
  try:
    response = requests.get(douyin_url, allow_redirects=False, headers=headers)
    return response.headers["Location"].split("/")[5]
  except Exception as e:
    print(str(e))
    print("Couldn't get douyin video id. "+douyin_url)
    return
  
def get_douyin_parsed_info(douyin_id):
  headers = {
      'authority': 'www.iesdouyin.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en-US,en;q=0.9',
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  }
  params = {
      'item_ids': douyin_id,
  }
  try:
    response = requests.get('https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/', params=params, headers=headers)
    result = response.json()

    if len(result["item_list"]) == 0:
      output = "Video Not Found!"
    else:
      output = ""
      direct_download_link = result["item_list"][0]["video"]['play_addr']['url_list'][0].replace("playvm","play")
      if "douyinstatic.com" in direct_download_link:
        AllImageURL = ""
        for image in result['item_list'][0]['images']:
          if AllImageURL == "":
            AllImageURL += image['url_list'][0]
          else:
            AllImageURL += "|ImageSep|"+image['url_list'][0]
        output += AllImageURL
      else:
        output += direct_download_link
        
      AuthorID = result['item_list'][0]['author']['unique_id']
      AuthorBackupID = result['item_list'][0]['author']['short_id']
      AuthorName = result['item_list'][0]['author']['nickname']
      Description = result['item_list'][0]['share_info']['share_title']
      LikeCount = result['item_list'][0]['statistics']['digg_count']
      Thumbnail = result['item_list'][0]['video']['cover']['url_list'][0]
      Duration = result['item_list'][0]['video']['duration']
      
      if AuthorID == "":
        output += "|||||" + str(AuthorBackupID)
      else:
        output += "|||||" + str(AuthorID)
      output += "|||||" + AuthorName
      output += "|||||" + Description
      output += "|||||" + str(LikeCount)
      output += "|||||" + Thumbnail
      output += "|||||" + str(Duration)
    return output
  except Exception as e:
    print(str(e))
    print("Couldn't parse douyin video info. "+douyin_id)
    return
    
  
def download_images(url,headers):
  if url!="":
    images_urls = url.split("|ImageSep|")
    for img_url in images_urls:
      try:
        r = requests.get(img_url, allow_redirects=True, headers=headers)
        open('image{}.jpg'.format(images_urls.index(img_url)), 'wb').write(r.content)
      except:
        pass
  else:
    print("Received Invalid download request: no URL given.")

def download_thumbnail(url,headers):
  if url!="":
    try:
      r = requests.get(url, allow_redirects=True, headers=headers)
    except:
      return download_thumbnail(url,headers)
    open('thumbnail.jpg', 'wb').write(r.content)
  else:
    print("Received Invalid download request: no URL given.")
    
def download_video(url,headers,tries=3):
  if url!="":
    try:
      r = requests.get(url, allow_redirects=True, headers=headers)
      open('video.mp4', 'wb').write(r.content)
    except:
      if tries <= 0:
        print("Failed to download this video multiple times. "+url)
        return 
      tries -= 1
      return download_video(url,headers,tries)
  else:
    print("Received Invalid download request: no URL given.")

def upload_befamous_cyou(directURL,Thumbnail,Description,video_info,Duration,headers):
    with open("douyin_downloads.txt",encoding='utf-8') as logFile:
      downloads = logFile.readlines()
    downloadedLink = ""
    for download in downloads:
      if video_info in download:
        downloadedLink = download.replace(video_info+"|X|X||Downloaded||X|X|","")
    if downloadedLink !="":
      download_video(directURL,headers)
      return downloadedLink
    
    download_video(directURL,headers)
    download_thumbnail(Thumbnail,headers)
    
    files = {'fileToUpload': open('video.mp4', 'rb')}
    data = {'file_extension': 'mp4'}
    upload_video = requests.post(upload_api, files=files,data=data)
    upload_video = upload_video.text.strip(" ").replace(directory_to_replace,"")
    #print(upload_video)
    files = {'fileToUpload': open('thumbnail.jpg', 'rb')}
    data = {'file_extension': 'jpg'}
    upload_thumbnail = requests.post(upload_api, files=files,data=data)
    upload_thumbnail = upload_thumbnail.text.strip(" ").replace(directory_to_replace,"")
    #print(upload_thumbnail)
    #os.remove("thumbnail.jpg")
  
    data = {'title': Description,'description': video_info,'thumbnail': upload_thumbnail,'duration': Duration,'video_location': upload_video,'size': str(os.path.getsize("video.mp4"))}
    add_video = requests.post(addvideo_api,data=data)
    #print(add_video.text.strip(" "))
    if "New record created successfully -> " in add_video.text:
      video_id = add_video.text.replace("New record created successfully -> ","").strip(" ")
      befamous_link = "https://befamous.cyou/watch/"+video_id
      with open("douyin_downloads.txt","a",encoding='utf-8') as logFile:
        logFile.write(video_info+"|X|X||Downloaded||X|X|"+befamous_link+"\n")
      return befamous_link
    else:
      print(add_video.text)
      return "Error! "+add_video.text


#Custom Use
async def get_channel_history(message,client):
  print("starting...")
  index = 0
  last_message = None
  while True:
    messages = await message.channel.history(limit=123,before=last_message).flatten()
    if len(messages) == 0:
      break
    for past_message in messages:
      last_message = past_message
      index += 1
      record = str(index) + " :: "
      if len(past_message.attachments) > 0:
        for attachment in past_message.attachments:
          record += attachment.url+ " :: "
      if past_message.content != "":
        record += past_message.content+ " ::end\n"
      with open("output.txt","a+",encoding='utf-8') as outputFile:
        outputFile.write(record)
  print("stopped at {}".format(index))
