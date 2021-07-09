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
from telethon.errors.rpcerrorlist import FloodWaitError, UserChannelsTooMuchError, UsernameNotOccupiedError

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

all_adding_accounts= [client1, client2, client3, client4, client5, client6]


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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_members(scraping_group))
    
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
    global all_adding_accounts
    # This will take all user from target group
    all_participants = []
    all_participants =  await client.get_participants(target_group, aggressive=True)
    all_participants_username = []
    for i in all_participants:
        if i.username is not None:
            all_participants_username.append(i.username)

    # This will create list of username which are there in csv file
    scraping_group_entity = await client.get_entity(scraping_group)
    users = []
    with open(f'{scraping_group_entity.title}.csv', encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        for row in rows:
            users.append(row[0])

    # created list for those who are added and those who aren't .
    added_user = []
    remaning_to_add_user = []    
    for i in users:
        if i in all_participants_username:
            added_user.append(i)
        else:
            remaning_to_add_user.append(i)

    added_member_count = len(added_user)
    target_group_entity = await client.get_entity(target_group)
    
    remaning_to_add_user_index = 0
    while True:
        for i in all_adding_accounts:
            adding_account_entity = await i.get_entity('me')
            print(adding_account_entity.first_name)
            adding_username = remaning_to_add_user[remaning_to_add_user_index]
            try:
                await add_user(added_member_count, i, adding_username, target_group_entity)
            except Exception as e:
                print(e)
            remaning_to_add_user_index += 1
            added_member_count +=1
        if len(all_adding_accounts):
            break







async def add_user(added_member_count, adding_user_info_list, adding_username, target_group_entity):
    global all_adding_accounts
    try:
        adding_account_entity = await adding_user_info_list.get_entity('me')
        print ("{}. Adding {} by {}".format(added_member_count, adding_username, adding_account_entity.first_name))
        user_to_add = await adding_user_info_list.get_entity(adding_username)
        await adding_user_info_list(InviteToChannelRequest(target_group_entity.title,[user_to_add]))
        print("Waiting for 10-30 Seconds")
        time.sleep(random.randrange(60, 90))
    except UserChannelsTooMuchError:
        print(f"{adding_account_entity.first_name} has added too many User in channel")
        all_adding_accounts.remove(adding_user_info_list)
    except FloodWaitError as e :
        print(f"This account has to wait for {e.seconds}, Because of Flood wait")
        all_adding_accounts.remove(adding_user_info_list)
        await asyncio.sleep(e.seconds)
        all_adding_accounts.append(adding_user_info_list)
    except PeerFloodError as e:
        print(e)
        all_adding_accounts.remove(adding_user_info_list)
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except UserNotMutualContactError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except UsernameNotOccupiedError:
        print("This username doesn't exist")
    except Exception as e:
        print(e)
        TracebackType.print_exc()
        
        

if __name__ == "__main__":
    main()
