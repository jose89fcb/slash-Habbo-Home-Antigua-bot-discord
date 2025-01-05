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
    name="habbohome", description="Escribe tu nombre.",
    options=[
        create_option(
            name="keko",
            description="Escribe tu nombre de Habbo Hotel.",
            option_type=3,
            required=True
        ),
        create_option(
            name="hotel",
            description="Elige el hotel",
            option_type=3,
            required=True,
            choices=[
                create_choice(name="ES - Hotel España", value="es"),
                create_choice(name="BR - Hotel Brasil", value="com.br"),
                create_choice(name="COM - Hotel Estados Unidos", value="com"),
                create_choice(name="DE - Hotel Alemán", value="de"),
                create_choice(name="FR - Hotel Francés", value="fr"),
                create_choice(name="FI - Hotel Finlandia", value="fi"),
                create_choice(name="IT - Hotel Italiano", value="it"),
                create_choice(name="TR - Hotel Turquía", value="com.tr"),
                create_choice(name="NL - Hotel Holandés", value="nl")
            ]
        )
    ]
)
async def _habbohome(ctx: SlashContext, keko: str, hotel: str):
    await ctx.defer()

    # Realizar la solicitud inicial
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko}")
    if response.status_code != 200:
        await ctx.send(f"Error al buscar información de {keko} en el hotel {hotel.upper()}. ❌")
        return

    # Obtener `idhabbo`
    try:
        idhabbo = response.json()['uniqueId']
    except KeyError:
        await ctx.send(f"No se encontró el usuario `{keko}` en Habbo {hotel.upper()}. ❌")
        return

    # Obtener identificador
    try:
        identificador = idhabbo.split("-")[-2]
    except IndexError:
        identificador = "❌"

    # Obtener `idcreador`
    photo_response = requests.get(f"https://www.habbo.{hotel}/extradata/public/users/{idhabbo}/photos")
    try:
        idcreador = photo_response.json()[0]['creator_id']
    except (IndexError, KeyError):
        idcreador = "❌"

    # Diccionario de banderas
    bandera_dict = {
        "es": "https://i.imgur.com/IplIfNP.png",
        "com.br": "https://i.imgur.com/YGQlPor.png",
        "nl": "https://i.imgur.com/fC8eIvR.png",
        "de": "https://i.imgur.com/vUgY11U.png",
        "fr": "https://i.imgur.com/CoLWbjf.png",
        "it": "https://i.imgur.com/va1X4j6.png",
        "com": "https://i.imgur.com/D6vwN9n.png",
        "com.tr": "https://i.imgur.com/wtiow4R.png",
        "fi": "https://i.imgur.com/BpQCpVi.png"
    }
    bandera = bandera_dict.get(hotel, "https://i.imgur.com/IplIfNP.png")

    # URL del póster
    url = f"https://images.habbo.com/web_images/mypages/{identificador}/{idcreador}.png"

    # Verificar si la imagen existe
    r = requests.get(url)
    if r.status_code == 200:
        imagen = Image.open(io.BytesIO(r.content))
        with io.BytesIO() as imagen_binary:
            imagen.save(imagen_binary, 'PNG')
            imagen_binary.seek(0)

            embed = discord.Embed(
                title=f"{keko}",
                url=f"https://habbo.{hotel}/home/{keko}",
                description=f"Aquí tienes la Habbo Home de `{keko}` de Habbo {hotel.upper()}",
                color=discord.Colour.random()
            )
            embed.set_image(url=f"attachment://HabboHomeAntigua.png")
            embed.set_thumbnail(url="https://images.habbo.com/c_images/album1584/HHOME.png")
            embed.set_footer(text=f"Habbo.{hotel}", icon_url=f"{bandera}")
            embed.set_author(name=f"HABBO HOME", icon_url=f"{bandera}")

            await ctx.send(
                f"Hola, {ctx.author.mention} este es el póster de {keko}",
                embed=embed,
                file=discord.File(fp=imagen_binary, filename=f'HabboHomeAntigua.png')
            )
    else:
        await ctx.send(f"{keko} no tiene póster ❌")

        



    

   
    
    


    
    






    
    
        
       
        
    

  
 
 
 
@bot.event
async def on_ready():
    print("BOT listo!")
    
bot.run(config["tokendiscord"])
