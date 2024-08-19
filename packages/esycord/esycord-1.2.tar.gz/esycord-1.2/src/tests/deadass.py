import esycord
esycord.Data
'''
bot=esycord.Bot('!',esycord.discord.Intents.all())
client = bot.client
voice=esycord.Voice(client=bot)


@bot.event()
async def on_ready():
    print(f'Logged in as {bot.user} and ID {bot.user.id}')
    print('-----------USE CTRL+C TO LOGOUT------------')
    await bot.set_bot_presence(state=discord.Status.dnd)

@bot.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        await voice.join(channel=ctx.author.voice.channel)
        await ctx.send('Connected to the voice channel!')
    else:
        await ctx.send('Not connected to any voice channel.')
    
@bot.command(pass_context=True)
async def send(ctx, url, msg):
    esycord.Webhook(webhook_url=url).send_message(message=msg)
    await ctx.send('Message sent to the webhook')





bot.run(token='MTE4ODM5ODExODc5OTE2NzU2OQ.GUHVML.cwLttEux3Qz1Oggu1CsM7cE3XyjwJ_bX8WsMx8')'''