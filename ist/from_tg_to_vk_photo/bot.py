import vk_api
import telebot
from telebot import types
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

BOT_TOKEN = "1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0"
VK_TOKEN = "1e6fc5ae345b2af29028971a82627158b07cff065db6d25f57ed113ebf333135469fb4ff8004dc6a50da0"
API_URL = "https://api.telegram.org/bot"
FILENAME = "Photo.jpg"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=["photo"])
def reply_message(message):
    file_info = bot.get_file(message.photo[2].file_id)
    file = bot.download_file(file_info.file_path)
    save_file(file)
    post_photo(file)
    bot.send_message(message.chat.id, text="test")

def post_photo(photo):
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    user_id = '216462892'
    upload = vk_api.VkUpload(vk_session)
    response = upload.photo_wall(R'C:\Users\Rekia\Desktop\IST\from_tg_to_vk_photo\Photo.jpg', user_id)
    api = vk_session.get_api()
    owner_id = response[0]['owner_id']
    photo_id = response[0]['id']
    api.wall.post(attachments=f'photo{owner_id}_{photo_id}')
    return response


def upload_photo(photo):
    get_upload_server_url = f"https://api.vk.com/method/photos.getWallUploadServer?access_token={VK_TOKEN}&v=5.131"
    response = requests.get(get_upload_server_url)
    result = response.json()["response"]

    uploaded_meta = upload_photo_to_server(result["upload_url"], photo)
    a = ''
    save_photo(uploaded_meta['server'], a, uploaded_meta['hash'])
    return result


def upload_photo_to_server(upload_url, photo):
    response = requests.post(upload_url, files=photo)
    return response.json()


def save_photo(server, photo, hash):
    url = f"https://api.vk.com/method/photos.saveWallPhoto?access_token={VK_TOKEN}&v=5.131server={server}&photo{photo}&hash={hash}"
    response = requests.get(url)
    result = response.json()
    return result


def save_file(file):
    with open(FILENAME, 'wb') as new_file:
        new_file.write(file)


bot.polling(non_stop=True)
