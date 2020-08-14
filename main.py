from pyrogram import Client, MessageHandler, Chat, Filters, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import requests
from subprocess import Popen, PIPE
import json
from bs4 import BeautifulSoup as bs
import wget

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# TOKEN = os.getenv("1141674372:AAFyGIGOME3ng7U9sl_NN99YscMOC_jG6ok")
TOKEN = os.getenv("1141674372:AAFyGIGOME3ng7U9sl_NN99YscMOC_jG6ok")

user_id = []

app = Client(
    "my_account",
    api_id=1667559,
    api_hash="1f7b5097aedb5dc887640673e01f02cb",
    bot_token=TOKEN
)

clown = 1023799889

def add_user(uid):
    if uid not in user_id:
        user_id.append(uid)

@app.on_message(Filters.command(["start", "help"]) & Filters.private)
def start(client, message):
    chat_id = message.from_user.id
    START = '''<b>Welcome To AnonFiles Bot❤️</b>

<b>I Can Upload/Download Files of Anonfiles.com</b>

<b>🌀To Upload FIles To Anonfiles Send The File as Document & To Download Files Send Me The Link of Anonfiles.</b>

<i>Feel Free To Use This Bot & Give Feedbacks To @MxClown.</i>'''
    app.send_message(chat_id, START, parse_mode="html")
    add_user(chat_id)

@app.on_message(Filters.document & Filters.private)
def upload(client, message):
    chat_id = message.from_user.id
    file_name = message.document.file_name
    username = message.from_user.username
    add_user(chat_id)
    try:
        download_start = app.send_message(chat_id, "<b>Downloading, Please Wait ❤️</b>\n<b>Big Files Takes More Time Don't Panic✌️</b>")

        dot = app.send_message(chat_id, "Downloading...")
        def progress(current, total):
            percent = f"{(current * 100) / total}%"
            downloaded = f"⚡️ **Downloaded :-** {percent}"
            app.edit_message_text(chat_id, dot.message_id, downloaded)
            
        app.download_media(message, progress=progress)
      
        app.edit_message_text(chat_id, download_start.message_id, "<b>✅Downloaded</b>\n<b>Uploading To </b>AnonFiles.com <b>:)</b>")
        app.delete_messages(chat_id, dot.message_id)
        
        
        change_dir = os.chdir("downloads")
        stdout = Popen(f'curl -F "file=@{file_name}" https://api.anonfiles.com/upload', shell=True, stdout=PIPE).stdout
        output = stdout.read()
        visit = json.loads(output)
        full_link = visit['data']['file']['url']['full']
        short_link = visit['data']['file']['url']['short']
        try:
            os.remove(file_name)
        except:
            pass
        anon_file_links = f'''❤️**Successfully Uploaded**

<b>Short Link -</b> {short_link}
<b>Full Link -</b> {full_link}
'''
        logs = f''' #Upload
        
@{username} Did Below Request

Short Link :- {short_link}
Full Link :- {full_link}'''

        
        app.send_message(chat_id, anon_file_links)
        app.send_message(clown, logs)
    except:
        app.send_message(chat_id, "<b>Unhandled Error!🤕</b>\n<b>Kindly Restart or Contact @MxClown👀️</b>")
        try:
            os.remove(file_name)
        except:
            pass

@app.on_message(Filters.command("broadcast") & Filters.private)
def broadcast(client, message):
    chat_id = message.chat.id
    if chat_id == clown:
        for uid in user_id:
            app.forward_messages(
                chat_id=uid,
                from_chat_id=message.chat.id,
                message_ids=message.reply_to_message.message_id,
                as_copy=True
            )
    

@app.on_message(Filters.command("users") & Filters.private)
def get_users(client, message):
    chat_id = message.from_user.id
    if chat_id == clown:
        total = "**Total users:** " + str(len(user_id))
        with open("users.txt", "w+") as f:
            f.write(str(user_id))
            f.close()
    
        try:
            app.send_document(chat_id, "users.txt", caption=total)
        except:
            pass

@app.on_message(Filters.command("stats") & Filters.private)
def stats(client, message):
    chat_id = message.from_user.id
    if chat_id == clown:
        total = "🌀 **Total users:** " + str(len(user_id))
        app.send_message(chat_id, total)


@app.on_message(Filters.text & Filters.private)
def download(client, message):
    chat_id = message.from_user.id
    user_message = message.text
    username = message.from_user.username
    if "anonfiles.com" in user_message:
        req = requests.get(user_message)
        if req.status_code == 200:
            data = bs(req.text, 'html.parser')
            download_link = data.find('a', {'id':'download-url'}).get('href')
            file_name = wget.detect_filename(download_link)
            reply = f'❤️Downloading **{file_name}**'
            downloading = app.send_message(chat_id, reply)
            wget.download(download_link)
            app.edit_message_text(chat_id, downloading.message_id, "✅ **Successfully Downloaded**. <i>Uploading File To Telegram</i>")
            app.send_document(chat_id, file_name, caption=file_name)
            app.delete_messages(chat_id, downloading.message_id)
            logs = f'''#Download
            
@{username} Did Below Request

File Name :- {file_name}
Link :- {download_link}'''

            app.send_message(clown, logs)
            try:
                os.remove(file_name)
            except:
                pass
        else:
            app.send_message(chat_id, "**Invalid Link...** Kindly Check Before Sending it \n🌀 **If You Think Its A Bug, Feel Free To Message ** @MxClown")
    else:
        app.send_message(chat_id, "<b>I Guess You're Lost😮</b>\n<b>Type /Help To Know What I Can do :)</b>\n<b>Join @ClownConfigs For Future Updates.❤️</b>")


app.add_handler(MessageHandler(start, Filters.command(["start", "help"]) & Filters.private))
app.add_handler(MessageHandler(get_users, Filters.command("users") & Filters.private))
app.add_handler(MessageHandler(broadcast, Filters.command("broadcast") & Filters.private))
app.add_handler(MessageHandler(stats, Filters.command("stats") & Filters.private))
app.add_handler(MessageHandler(upload, Filters.document & Filters.private))
app.add_handler(MessageHandler(download, Filters.text & Filters.private))
app.run()
