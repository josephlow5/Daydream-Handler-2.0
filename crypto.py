import urllib.request
import json
import discord
import random

CryptoPrefixs = ['gg','GG','Gg']

def random_market_info():
  url_list = ["https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin","https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum","https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=dogecoin","https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=litecoin","https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=cardano"]
  url = random.choice(url_list)
  try:
    result = urllib.request.urlopen(url).read()
    if(result):
      result_dict = json.loads(result)
      coin_id = result_dict[0]["id"]
      price = '$'+str(result_dict[0]['current_price'])
      return(coin_id + " : " + price)
  except:
    pass
  return "Error!"
    
async def on_message(message, client):
  for prefix in CryptoPrefixs:
    if message.content.startswith(prefix):
      if message.channel.id == 844764717620920330:
        await message.delete()
        args = message.content.replace(prefix+" ",'')
        
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+args  #Use Everything you typed

        #Custom Shortform
        if 'btc' == args:
          url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"
        if 'eth' == args:
          url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum"
        if 'doge' == args:
          url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=dogecoin"
        if 'ltc' == args:
          url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=litecoin"
        if 'ada' == args:
          url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=cardano"
        
        try:
          result = urllib.request.urlopen(url).read()
          if(result):
            result_dict = json.loads(result)
            
            embedVar = discord.Embed(title=result_dict[0]["name"] + " | " + result_dict[0]["id"] + " || Current Market Price", description="We provide real-time price of cryptocurrencies, type command gg followed by api id (up there after '|') to get result.\nAll information provided by coingecko.com", color=0x42daf5)
            embedVar.set_thumbnail(url=result_dict[0]['image'])
            embedVar.set_footer(text='Powered by ShareTheFreeFun Digitals <https://discord.gg/y6e4hCybmE>')
            embedVar.add_field(name="Current Price", value='$'+str(result_dict[0]['current_price']))  
            embedVar.add_field(name="Highest @ Last 24 Hours", value='$'+str(result_dict[0]['high_24h']))  
            embedVar.add_field(name="Lowest @ Last 24 Hours", value='$'+str(result_dict[0]['low_24h']))  
            embedVar.add_field(name="Price Change @ Last 24 Hours", value=str(result_dict[0]['price_change_percentage_24h'])+"%")  
            embedVar.add_field(name="Currently featured Cryptos", value='btc, eth, doge, ltc, ada')
            embedVar.add_field(name="Currently supported Cryptos", value='[Click the coin and find API id](https://www.coingecko.com/en/coins/all)')

            await message.channel.send(embed=embedVar)
        except:
          await message.channel.send("Sorry, API error or the coin is not supported!")