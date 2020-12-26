from server import keep_alive
from replit import db
import requests
import discord
import asyncio
import os

client = discord.Client()


def get_stock(item):
    s = requests.Session()

    url = f"https://api.bestbuy.com/v1/products((search={item})&(categoryPath.id=abcat0507002))"

    payload = {
        "apiKey":
            os.getenv('BESTBUY_API_KEY'),
        "sort":
            "name.asc",
        "show":
            "name,inStoreAvailability,onlineAvailability,regularPrice,salePrice,thumbnailImage,inStoreAvailabilityText,onlineAvailabilityText,url",
        "pageSize":
            99,
        "format":
            "json",
    }
    headers = {}
    r = s.get(url, headers=headers, params=payload)
    j = r.json()
    return j["products"]


def update_items(item):
    if "items" in db.keys():
        items = db["items"]
        items.append(item)
        db["items"] = items
    else:
        db["items"] = [item]


def delete_items(index):
    items = db["items"]
    if len(items) > index:
        del items[index]
    db["items"] = items


@client.event
async def on_ready():
    print(f'We have logged in as {client.user} ')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$add'):
        item_to_add = msg.split("$add ", 1)[1]
        update_items(item_to_add)
        await message.channel.send(
            f":tada: Added {item_to_add} to the list! :tada:")

    if msg.startswith('$del'):
        items = []
        if "items" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_items(index)
            items = db["items"]
        await message.channel.send(items)

    if msg.startswith('$list'):
        items = []
        if "items" in db.keys():
            items = db['items']
        await message.channel.send(items)

    if msg.startswith('$test'):
        test_msg = msg.split("$test ", 1)[1]
        j = get_stock(test_msg)
        print(j)
        await message.channel.send(j)

    if msg.startswith('$timer'):
        timer = db['timer']
        await message.channel.send(
            f'[INFO] Timer is currently {timer} seconds :robot:')

    if msg.startswith('$settimer'):
        time_new = int(msg.split('$settimer ', 1)[1])
        db['timer'] = time_new
        await message.channel.send(f'[INFO] Timer was changed to {time_new} :thumbsup:')

    if msg.startswith('$run'):
        in_store_availability = False
        online_availability = True
        final = ''
        test_list = []
        db["running"] = True
        if "items" in db.keys():
            while db['running']:
                items = db['items']
                print(f"[DEBUG] Checking for {items}")
                for item in items:
                    results = get_stock(item)
                    for r in results:
                        if r["inStoreAvailability"]:
                            final += f'\n[Best Buy] - {r["name"]} - Available in store for {r["regularPrice"]}'
                            in_store_availability = True
                        else:
                            in_store_availability = False

                        if r["onlineAvailability"]:
                            final += f'\n[Best Buy] - {r["name"]} - Available online for {r["regularPrice"]} at {r["url"]}'
                            online_availability = True
                        else:
                            online_availability = False

                    test_list.extend([{
                        "name": "Item",
                        "value": item,
                        "inline": True
                    },
                        {
                            "name": "In Store",
                            "value": in_store_availability,
                            "inline": True
                        },
                        {
                            "name": "Online",
                            "value": online_availability,
                            "inline": True
                        }])

                # space_list = [{"name": '\u200b', "value": '\u200b', "inline": False}]

                final_dict = {
                    "color": 0x0099ff,
                    "title": 'Live Stock Bot',
                    "description": "Checking for RTX cards",
                    "fields": test_list,
                    "footer": {
                        "text": "Best Buy"
                    }
                }
                embed = discord.Embed.from_dict(final_dict)
                await message.channel.send(embed=embed)

                test_list = []

                if final:
                    await message.channel.send(final)
                    final = ''

                await asyncio.sleep(int(db['timer']))

    if msg.startswith('$stop'):
        db['running'] = False


keep_alive()
client.run(os.getenv('TOKEN'))
