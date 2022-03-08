import discord
import os
import json
from discord.ext import commands, tasks
from genshinusers import Users, load_G_users
from wordoftheday import get_wotd

TOKEN = os.environ['token']
client = commands.Bot(command_prefix='!')


Moderators = {}
Moderateds = {}
@client.event
async def on_reaction_add(reaction, user):
    
    msg_sender = reaction.message.author
    msg_content = reaction.message.content
    msg = reaction.message

    emojis = {
    ':thisisameme:': '<:thisisameme:936493541453090857>',
    ':thisisavideo:': '<:thisisavideo:936493623074250772>',
    ':YEP:': '<:YEP:936618774860275743>'
    }
    
    def appendModList():
        try:
            Moderators[user] += 1
        except:
            Moderators[user] = 1
        try:
            Moderateds[msg_sender] += 1
        except:
            Moderateds[msg_sender] = 1

    # Removes messages that were supposed to be either in the video,
    # or meme channel and re-sends them in their proper channels.
    if str(reaction.emoji) == emojis[':thisisameme:']:
        attachment = msg.attachments[0].url
        await msg.delete()
        await in_channel('#memes').send(f'sent by: {msg_sender} {attachment}')
        appendModList()
    elif str(reaction.emoji) == emojis[':thisisavideo:']:
        await msg.delete()
        await in_channel('#videos').send(f'sent by: {msg_sender} {msg_content}')
        appendModList()
    # //



@client.command()
async def checkresin(ctx):
    user = Users.get_object_by_discordID(ctx.author.id)

    try:
        resin = user.get_resin_count()
        await ctx.send(f'Your resin count is at : {resin}/160')
    except:
        await ctx.send('Error! Cannot fetch resin count.')

@client.command()
async def addaccount(ctx, *args):    
    Users(ctx.author.id, *[i for i in args])


last_wotd_ID = 950585269017509948
@tasks.loop(hours=12)
async def get_word_of_day():
    global last_wotd_ID
    wotd_data = get_wotd()
    Word = wotd_data['word']
    Definition = wotd_data['definition']
    Example = wotd_data['example']
    
    if await wotd_alread_sent(Word):
        return 1
    
    message = discord.Embed(
        title = "Word of the day!",
        description = "Merriam-Webster's word of the day",
        colour = discord.Colour.green()
    )
    message.set_footer(text='https://www.merriam-webster.com/word-of-the-day')
    message.add_field(name=f'{Word}:', value=Definition, inline=False)
    message.add_field(name='Example:', value=Example, inline=False)

    sent_msg = await in_channel('#wotd').send(embed=message)

    last_wotd_ID = sent_msg.id

@get_word_of_day.before_loop
async def before():
    await client.wait_until_ready()  

async def wotd_alread_sent(current_word):
    channel = in_channel('#wotd')
    msg = await channel.fetch_message(last_wotd_ID)
    msg_wotd = msg.embeds[0].fields[0].name

    print(msg_wotd)
    if msg_wotd == f'{current_word}:':
        return True
    
    return False



def in_channel(channel_key):
    channels = {
    '#memes': 889091921962745876,
    '#videos': 889091905240055848,
    '#freemo': 928591987018440724,
    '#bot-testing': 941681794812616764,
    '#wotd': 948389047208935484
    }

    return client.get_channel(channels[str(channel_key)])


if __name__ == '__main__':
    load_G_users()
    get_word_of_day.start()
    client.run(TOKEN)