from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

## ASAGIYA YAZMANIZ GEREKEN SATIRLARI "my.telegram.org" ADRESINDEN ALMALISINIZ!

api_id = 123456   
api_hash = 'API_HASH_DEGERINIZ'
phone = '+111111111111'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Giris kodunu yazin: '))

input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Uyeleri ekleyeceginiz grubu secin:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input("Sayi girin: ")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

mode = int(input("Uyeleri kullanici adi ile eklemek icin 1, IDleri ile eklemek icin 2 yazin."))

n = 0

for user in users:
    n += 1
    if n % 50 == 0:
    sleep(900)
    try:
        print ("Ekleniyor {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Secilen mod mevcut degil, lutfen tekrar deneyin.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("60-180ms arasi bekleniyor...")
        time.sleep(random.randrange(60, 180))
    except PeerFloodError:
        print("Telegram tarafindan spam hatasi alindi. Bot simdilik durdurulacak. Daha sonra tekrar deneyin.")
    except UserPrivacyRestrictedError:
        print("Kullanicinin guvenlik ayarlari gruplara eklenmesine izin vermiyor. Diger kullaniciya geciliyor.")
    except:
        traceback.print_exc()
        print("Belirsiz bir hata olustu!")
        continue
