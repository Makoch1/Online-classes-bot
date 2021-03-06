import discord
import os
import json
from discord.ext import commands, tasks
from genshinusers import Users, load_G_users
from wordoftheday import get_wotd

TOKEN = os.environ.get("Token")
client = commands.Bot(command_prefix='!')


@client.event
async def on_reaction_add(reaction, user):
    msg_sender = reaction.message.author
    msg_content = reaction.message.content
    msg = reaction.message

    emojis = {
    ':thisisameme:': '<:thisisameme:936493541453090857>',
    ':thisisavideo:': '<:thisisavideo:936493623074250772>',
    }

    if str(reaction.emoji) == emojis[':thisisameme:']:
        try:
            content = msg.attachments[0].url
        except:
            content = msg_content

        await in_channel('#memes').send(f'sent by: {msg_sender} {content}')
        await msg.delete()

    elif str(reaction.emoji) == emojis[':thisisavideo:']:
        try:
            content = msg.attachments[0].url
        except:
            content = msg_content

        await in_channel('#videos').send(f'sent by: {msg_sender} {content}')
        await msg.delete()



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
    message = await get_last_wotd(channel)
    try:
        msg_wotd = message[0].fields[0].name
    except:
        print('word not found')
        msg_wotd = None
    print(msg_wotd)
    if msg_wotd == f'{current_word}:':
        return True
    
    return False

async def get_last_wotd(channel):
    async for msg in channel.history(limit=100):
        if msg.author == client.user:
            return msg.embeds
    return None


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
