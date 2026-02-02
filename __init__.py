import helper.fetchDeals as fetcher
# import helper.saver as saver
import helper.discordLogic as discordLogic
import helper.parser as parser
import configuration as conf
import discord
import requests

def readablePrices(idsToGames, priceData):
    readableForm = idsToGames[priceData['id']] + ':\n'
    readableForm += ' Lowest price the game ever had - ' + str(priceData['historyLow']['all']['amount']) + priceData['historyLow']['all']['currency'] + '\n'
    readableForm += ' Current deals: \n'
    for deal in priceData['deals']:
        readableForm += '     ' + deal['shop']['name'] + ': ' + str(deal['price']['amount']) + deal['price']['currency'] + '\n'
        readableForm += '       link: ' + deal['url'] + '\n'
    readableForm += '\n'
    return readableForm

def printDeals(deal):
    for data in deal:
        print(data['title'] + ':')
        print(' Regular price: ', data["regular"]["amount"], data["regular"]["currency"])
        print(' Current price: ', data["price"]["amount"], data["price"]["currency"])
        print('!!! ', data['cut'], '% !!!')
        print(data['url'])
        print('\n')

def printPrices(idsToGames, priceData):
    print(idsToGames[priceData['id']] + ':')
    print(' Lowest price - ', priceData['historyLow']['all']['amount'], priceData['historyLow']['all']['currency'])
    print(' Current deals: ')
    for deal in priceData['deals']:
        print('     ', deal['shop']['name'], ': ', deal['price']['amount'], deal['price']['currency'])
        print('       link: ', deal['url'])
    print('\n')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if not message.content.lower().startswith("!deal "):
        return

    query = message.content[6:].strip().split(' && ')
    channel = client.get_channel(conf.TARGET_CHANNEL_ID)

    if not query:
        await channel.send(f"{message.author.mention} please provide a game name.")
        return

    # 1. Search game
    try:
        gamesToIds = fetcher.resolve_steam_app_ids(query)
        idsToGames = parser.create_reverse_map(gamesToIds)
        ids = parser.extract_ids(gamesToIds)
    except Exception as e:
        await channel.send(f"{message.author.mention} error searching for game(s).")
        return

    if not len(ids):
        await channel.send(f"{message.author.mention} no results found for **{query}**.")
        return

    # 2. Fetch prices
    priceMessageToDiscord = ""
    try:
        prices = fetcher.get_prices(ids)

        for priceData in prices:
            if priceData['id'] in ids:
                priceMessageToDiscord += readablePrices(idsToGames, priceData)
    except Exception:
        await channel.send(f"{message.author.mention} error fetching prices.")
        return

    if not prices:
        await channel.send(
            f"{message.author.mention} {"This" if len(query) == 1 else "These"} games have no active deals right now."
        )
        return

    # 3. Pick best deal
    # best = min(deals, key=lambda d: d["price"]["amount"])
    #
    # price = best["price"]["amount"]
    # store = best["shop"]["name"]
    # url = best["url"]

    # 4. Send result
    await channel.send(priceMessageToDiscord, suppress_embeds=True)


client.run(conf.DISCORD_BOT_TOKEN)

# if __name__ == "__main__":

    # games = ['Outer Wilds', 'ARC Raiders', 'Spelunky']
    # gamesToIds = fetcher.resolve_steam_app_ids(games)
    # idsToGames = parser.create_reverse_map(gamesToIds)
    # ids = parser.extract_ids(gamesToIds)
    #
    # prices = fetcher.get_prices(ids)
    #
    # priceMessageToDiscord = ""
    # for index, priceData in enumerate(prices):
    #     if priceData['id'] in ids:
    #         # printPrices(idsToGames, priceData)
    #         priceMessageToDiscord += readablePrices(idsToGames, priceData)

    # Get deals unrelated to hardcoded games
    # deals = fetcher.get_deals(False)
    # printDeals(parser.extract_deals(deals))

    # Print deals for hardcoded games
    # discordLogic.post_to_discord(priceMessageToDiscord)



