import discord
from discord.ext import commands
import json
import requests
import time
from PIL import Image, ImageDraw, ImageFont, ImageFile
import io
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext


with open("configuracion.json") as f: #Creamos un archivo de configuracion para el bot
    config = json.load(f)

intents = discord.Intents.all()
 
bot = commands.Bot(command_prefix='!', description="ayuda bot") #Comando
bot.remove_command("help") # Borra el comando por defecto !help
slash = SlashCommand(bot, sync_commands=True)
@slash.slash(
    name="habbo", description="Escribe tu nombre.",
    options=[
                create_option(
                  name="habbonombre",
                  description="Escribe tu nombre de habbo hotel.",
                  option_type=3,
                  required=True
                ),
                 create_option(
                  name="hotel",
                  description="Elige él hotel",
                  option_type=3,
                  required=True,
                  choices=[
                      create_choice(
                          name="ES",
                          value="es"
                      ),
                      create_choice(
                          name="BR",
                          value="com.br"
                      ),
                      create_choice(
                          name="COM",
                          value="com"
                      ),
                      create_choice(
                          name="DE",
                          value="de"
                      ),
                      create_choice(
                          name="FR",
                          value="fr"
                      ),
                      create_choice(
                          name="FI",
                          value="fi"
                      ),
                      create_choice(
                          name="IT",
                          value="it"
                      ),
                      create_choice(
                          name="TR",
                          value="com.tr"
                      ),
                      create_choice(
                          name="NL",
                          value="nl"
                      )
                  ]
                
               
                  
                )
             ])
             
            
             

    


async def _habbo(ctx:SlashContext, habbonombre:str,hotel:str):
    await ctx.defer()
 

 


   
    

    ####
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={habbonombre}")
    try:

     idhabbo = response.json()['uniqueId']
    except KeyError:
     idhabbo="❌"
    try:

     identificador = response.json()['uniqueId'].split("-")[-2]
    except KeyError:
        identificador="❌"

    response = requests.get(f"https://www.habbo.{hotel}/extradata/public/users/{idhabbo}/photos")
    try:

     idcreador = response.json()[0]['creator_id']
    except IndexError:
        idcreador="❌"

   

   
    

   
    
    url = f"https://images.habbo.com/web_images/mypages/{identificador}/{idcreador}.png" #url
    
    
    
    r = requests.get(url)
    if  r.status_code ==200:
        imagen = Image.open(io.BytesIO(requests.get(url).content))
        with io.BytesIO() as imagen_binary:
            imagen.save(imagen_binary, 'PNG')
            imagen_binary.seek(0)
            

            embed = discord.Embed(title="Habbo Home", description=f"Aquí tienes la Habbo Home de `{habbonombre}` de Habbo {hotel.upper()}")
            embed.set_image(url=f"attachment://HabboHomeAntigua.png")
            
            embed.set_thumbnail(url="https://images.habbo.com/c_images/album1584/HHOME.png")
           

         
            
            await ctx.send(f"Hola, {ctx.author.mention} este es el póster de {habbonombre}",embed=embed,file=discord.File(fp=imagen_binary, filename=f'HabboHomeAntigua.png'))
            

    else:
        await ctx.send(f"{habbonombre} no tiene póster ❌")
        



    

   
    
    


    
    






    
    
        
       
        
    

  
 
 
 
@bot.event
async def on_ready():
    print("BOT listo!")
    
bot.run(config["tokendiscord"])
