
import os
import discord
from discord.ext import commands, tasks
import aiohttp

# IMPORTANTE: Use variáveis de ambiente seguras para o TOKEN
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

async def pegar_dados_wemix():
    url = 'https://api.coingecko.com/api/v3/coins/wemix-token?localization=false&tickers=false&market_data=true'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            preco = data['market_data']['current_price']['usd']
            variacao = data['market_data']['price_change_percentage_24h']
            return preco, variacao

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    atualizar_status.start()

@tasks.loop(seconds=60)
async def atualizar_status():
    try:
        preco, variacao = await pegar_dados_wemix()
        simbolo = "⬆️" if variacao >= 0 else "⬇️"
        status = f'WEMIX: ${preco:,.4f} {simbolo}'
        await bot.change_presence(activity=discord.Game(name=status))
    except Exception as e:
        print(f'Erro ao atualizar status: {e}')

@bot.command(name='preco')
async def preco(ctx):
    try:
        preco, variacao = await pegar_dados_wemix()
        simbolo = "⬆️" if variacao >= 0 else "⬇️"
        mensagem = f"**📈 WEMIX**: ${preco:.4f} ({variacao:+.2f}%) {simbolo}"
        await ctx.send(mensagem)
    except Exception as e:
        await ctx.send("Erro ao buscar preço do WEMIX.")
        print(f'Erro: {e}')

bot.run(TOKEN)
