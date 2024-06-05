import discord
import json
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='=', intents=intents)

warnings = {}
try:
    with open('warnings.json', 'r') as infile:
        warnings = json.load(infile)
except:
    print("pas de fichier warnings")        

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("je suis là"))
    print("coucou")
    
#commandes =regles
@bot.command()
async def regles(ctx):
    await ctx.send("Voici les règles de notre serveur Discord !\n1. Gentil\n2. Pas Méchant\n3. J'ai plus d'idée")
    
#commandes =bienvenue
@bot.command()
async def bienvenue(ctx, nouveau_membre: discord.Member):
    pseudo = nouveau_membre.mention
    await ctx.send(f"Bienvenue {pseudo}! N'oublie pas de faire =regles")
    
#traitement d'erreur bienvenue
@bienvenue.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("=bienvenue @user")

#detecter les emojis pour le role python
@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name #recupere le nom de l'emoji
    canal = payload.channel_id #recupere le numero du salon 
    message = payload.message_id #recupere l'id du message
    python_role = get(bot.get_guild(payload.guild_id).roles, name="python")
    membre = await bot.get_guild(payload.guild_id).fetch_member(payload.user_id)
    
    if canal == 1247962420211617793 and message == 1247962781412622366 and emoji == "python":
        await membre.add_roles(python_role)
        await membre.send("Grade données !")
        
@bot.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji.name #recupere le nom de l'emoji
    canal = payload.channel_id #recupere le numero du salon 
    message = payload.message_id #recupere l'id du message
    python_role = get(bot.get_guild(payload.guild_id).roles, name="python")
    membre = await bot.get_guild(payload.guild_id).fetch_member(payload.user_id)
    
    if canal == 1247962420211617793 and message == 1247962781412622366 and emoji == "python":
        await membre.remove_roles(python_role)
        await membre.send("Grade retiré !")

#commande warning
@bot.command()
@commands.has_role("python")
async def warning(ctx, membre: discord.Member):
    id = membre.id

    #rajoute un warning a l'utilisateur
    if id not in warnings:
        warnings[id] = 0
        
    warnings[id] += 1 
    
    if warnings[id] >= 3:
        await membre.send(f"Bye {pseudo} :D !")
        await membre.kick()
    else:      
        pseudo = membre.mention
        await ctx.send(f"Attention {pseudo} tu va être punis")
        
    with open('warnings.json', 'w+') as outfile:
        json.dump(warnings, outfile)
    
@warning.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("=warning @user") 

token = "rentrer_token_bot"

print("lancement du bot ...")

#connection au serveur
bot.run(token)

