import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

import Server_Checker


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY_MINECRAFT')


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents) # Prefijo del Bot


@bot.event
async def on_ready():
    print('¡Bot listo!')
    try:
        sinc = await bot.tree.sync() 
        print(f'¡Sincronizados {len(sinc)} comandos!')
    except Exception as e:
        await print(f'Error: La sincronización falló. {str(e)}')
    await channel_refresh((True, 30), 1160197151431872533)


@bot.tree.command(name='ip', description='Sabrás la IP del servidor')
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} ¡La ip es **analand.net**!", ephemeral = True)


@bot.tree.command(name='status', description='Sabrás el estado del servidor :)')
async def status_command(interaction: discord.Interaction):
    voice_channel = bot.get_channel(int(1160197151431872533))
    if Server_Checker.refrescar(API_KEY, 'https://minecraft-mp.com/api/?object=servers&element=detail&key=').serverStatus:
        await interaction.response.send_message(f"Analand está **ONLINE** 💚")
        await voice_channel.edit(name='𝗢𝗡𝗟𝗜𝗡𝗘 💚')
    else:
        await interaction.response.send_message(f"Analand está **OFFLINE** 💔") 
        await voice_channel.edit(name='𝗢𝗙𝗙𝗟𝗜𝗡𝗘 💔')



@bot.command(name='sync')
async def sincronizar(ctx):
    try:
        result = await bot.tree.sync()  # Make sure this is a coroutine
        if result:  # Check if the sync was successful
            await ctx.send('¡Listo!')
        else:
            await ctx.send('La sincronización falló.')
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')


async def channel_refresh(channel_refresh_data: list, channel_id: int):
    channel_refresh_data = channel_refresh_data
    channel_id = channel_id  
    while True:
        await asyncio.sleep(channel_refresh_data[1]) # Espera x tiempo antes de ejecutar el código
        channel = bot.get_channel(channel_id)
        if not channel:
            print(f'No se pudo encontrar el canal con ID {channel_id}')
            continue

        if channel_refresh_data[0]:
            server_status = Server_Checker.refrescar(API_KEY, 'https://minecraft-mp.com/api/?object=servers&element=detail&key=').serverStatus
            hora_actual = datetime.now()
            if server_status:
                await channel.edit(name=f'𝗢𝗡𝗟𝗜𝗡𝗘 💚 - {hora_actual.strftime("%H:%M")}')
                print('Canal actualizado: En línea')
            else:
                await channel.edit(name=f'𝗢𝗙𝗙𝗟𝗜𝗡𝗘 💔 - {hora_actual.strftime("%H:%M")}')
                print('Canal actualizado: Fuera de línea')

ban_message = [None, False]

@bot.event
async def on_message(message, message_limit: int = 10):
    bot_id = 1179183192914272276
    integration_id = 1010247664455122985
    channel_id = 1179361990599245934
    message_id_author = message.author.id

    # Verifica si el mensaje se envió en un canal específico
    if message.channel.id == channel_id:  # Reemplaza TU_CANAL_ID con el ID de tu canal
        if message_id_author != bot_id and message_id_author != integration_id:
            #await message.author.ban()

            # Elimina los últimos mensajes del usuario en el canal
            async for msg in message.channel.history(limit=message_limit,):  # Puedes ajustar el límite según tus necesidades
                if msg.author == message.author:
                    await msg.delete() # Elimina el mensaje del canal anti-raid
                    await eliminar_mensajes(message, message.author.name) # Elimina todos los mensajes del servidor

            # Envía un mensaje indicando el ban
            if not ban_message[1]:
                ban_message[0] = await message.channel.send(f"{message.author.mention} ha sido baneado por escribir aquí.")
                ban_message[1] = True

                await asyncio.sleep(5)
                await ban_message[0].delete()
                ban_message[1] = False

def change_time(hora_input):
    hora_actual = hora_input
    hora = int(hora_actual[0:1])
    delta_time = 1
    return f'{hora + delta_time}:{hora_actual[3:6]}'

def get_all_members():
    for guild in bot.guilds:
        for member in guild.members:
            yield member

async def eliminar_mensajes(interaction, username) -> str:
    # Obtenemos la hora actual
    now = datetime.utcnow()
    # Restamos 10 minutos a la hora actual
    ten_minutes_ago = now - timedelta(minutes=10)
    # Buscamos al usuario por su nombre
    for user in get_all_members():
        if username == str(user):
            break
        else:
            user = None
    if not user:
        return None

    # Recorremos todos los canales de texto del servidor
    resultado = ''
    messages = []
    for channel in interaction.guild.text_channels:
        async for message in channel.history(after=ten_minutes_ago):
            if message.author == user:
                messages.append(message)
        # Intentamos borrar los mensajes
        try:
            # Utilizamos la función purge para borrar los mensajes
            await channel.purge(after=ten_minutes_ago, check=lambda msg: str(msg.author.name) == username, oldest_first=True)
            if len(messages) > 0:
                resultado = f'{resultado}\n · {len(messages)} Mensajes de {user} eliminados en {channel} desde las {change_time(messages[0].created_at.strftime("%H:%M"))}'
                messages.clear()
        except discord.Forbidden:
            continue
    return str(resultado)

@bot.tree.command(name= 'purga')
@app_commands.describe(
    usuario='Nombre del usuario del que se van a eliminar los mensajes'
)
async def add(interaction: discord.Interaction, usuario: str):
    # Responder inmediatamente
    await interaction.response.send_message('· `Procesando...`', ephemeral=False) # Primera respuesta
    # Realizar la operación de larga duración

    resultado = await eliminar_mensajes(interaction, usuario)

    # Editar el mensaje de respuesta con el resultado
    if resultado is not None:#Entra aqui y no rompe si encuetra mensaje
        await interaction.edit_original_response(content=f'**Mensajes Eliminados de {usuario}:**\n```{resultado}```') # Edición de respuesta
    else:
        await interaction.edit_original_response(content='Ese usuario no existe :(')

bot.run(TOKEN)