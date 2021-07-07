import asyncio
import logging
from os import urandom
from time import process_time_ns
import time
from types import TracebackType
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.sync import TelegramClient
from csv import writer
import csv
from telethon.tl.functions.channels import InviteToChannelRequest
import random
from telethon.tl.types import InputPeerChannel
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                   level=logging.INFO)
from datetime import datetime
from telethon.errors.rpcerrorlist import UserNotMutualContactError
from telethon.errors.rpcerrorlist import FloodWaitError, UserChannelsTooMuchError

# +918931081907 - A1
api_id1 = 6095862
api_hash1 = '0b06a3e134908dc7fc49534177bd1698'

# +916352921999 - A2
api_id2 = 6341990
api_hash2 = '872ea84216b8c1a2415448db8f33e80c'

# +918320052578 - y D
api_id3 = 6135622
api_hash3 = '31b0db73788064a6a974c725fa2a43c2'


# +919541837249 - A4
api_id4 = 6454392
api_hash4 = '16f8f7d8811cd3eae8afb5b18b1b65c4'


# +918084374648 - A5
api_id5 = 6916656
api_hash5 = 'c5def0df65230a5107d4ade46e467db2'



# +918853210160 - A6
api_id6 = 6532409
api_hash6 = '6ebfd18cca2b1dc6bebcd42f6164e922'




api_id = 5911805
api_hash = 'baf59bae0d7caba308cdada2079670c2'

client = TelegramClient("MAIN", api_id, api_hash)
client1 = TelegramClient("+918931081907", api_id1, api_hash1)
client2 = TelegramClient("+916352921999", api_id2, api_hash2)
client3 = TelegramClient("+918320052578", api_id3, api_hash3)
client4 = TelegramClient("+919541837249", api_id4, api_hash4)
client5 = TelegramClient("+918084374648", api_id5, api_hash5)
client6 = TelegramClient("+918853210160", api_id6, api_hash6)



def main():
    client.start()
    client1.start()
    client2.start()
    client3.start()
    client4.start()
    client5.start()
    client6.start()

    print("Userbot on!")

    scraping_group = 'https://t.me/SRTMSG'
    target_group = 'https://t.me/cloudcitysg'
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(scrape_members(scraping_group))
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_members(scraping_group, target_group))
    
    client.disconnect()
    client1.disconnect()
    client2.disconnect()
    client3.disconnect()
    client4.disconnect()
    client5.disconnect()
    client6.disconnect()




async def scrape_members(scraping_group):
    
    all_participants = []
    all_participants =  await client.get_participants(scraping_group, aggressive=True)
    scraping_group_entity = await client.get_entity(scraping_group)
    with open(f"{scraping_group_entity.title}.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        for user in all_participants:
            accept=True
            try:
                lastDate=user.status.was_online
                num_months = (datetime.now().year - lastDate.year) * 12 + (datetime.now().month - lastDate.month)
                if(num_months>1):
                    accept=False
            except:
                continue
            if accept:
                if user.username:
                    username= user.username
                    writer.writerow([username])      
    print('Members scraped successfully.')






async def add_members(scraping_group, target_group):
    

    added_member = 0
    all_participants = []
    all_participants =  await client.get_participants(target_group, aggressive=True)
    all_participants_username = []
    for i in all_participants:
        if i.username is not None:
            all_participants_username.append(i.username)
    all_accounts = [client1, client2, client3, client4, client5, client6]
    scraping_group_entity = await client.get_entity(scraping_group)
    users = []
    with open(f'{scraping_group_entity.title}.csv', encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        for row in rows:
            user = {}
            user['username'] = row[0]
            users.append(user)
    print('Choose a group to add members:')
    target_group_entity = await client.get_entity(target_group)
    account_index = 0
    
    for count, user in enumerate(users):
        if user['username'] in all_participants_username:
            added_member += 1
            print(str(added_member) + ". " +user['username'] + ' is already added.')
        else:
            added_member += 1
            try:
                adding_account_entity = await all_accounts[account_index].get_entity('me')
                print ("{}.Adding {} by {}".format(added_member, user['username'], adding_account_entity.first_name))
                user_to_add = await all_accounts[account_index].get_entity(user['username'])
                await all_accounts[account_index](InviteToChannelRequest(target_group_entity.title,[user_to_add]))
                print("Waiting for 10-30 Seconds...")
                time.sleep(random.randrange(20, 30))
            except UserChannelsTooMuchError:
                print("This account has added too many User in channel")
                account_index +=1
                if account_index == 6:
                    print('adding capacity over')
                    break
            except FloodWaitError as e :
                print(f"This account has to wait for {e.seconds}")
                account_index +=1
                if account_index == 6:
                    print('adding capacity over')
                    break
            except PeerFloodError as e :
                print(f"This account has to wait for {e.seconds}")
                account_index +=1
                if account_index == 6:
                    print('adding capacity over')
                    break
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
                continue
            except UserNotMutualContactError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
                continue
            except Exception as e:
                print(e)
                TracebackType.print_exc()
                continue
            if added_member == 500:
                break






if __name__ == "__main__":
    main()
