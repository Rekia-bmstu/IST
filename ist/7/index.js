const telegramBotToken = '1519877833:AAEvxH9lIh94nbLptcahXWvuU_wbURsEZm0';

async function getMessagesButtonClicked() {
    const updates = await getTelegramUpdates();

    const photoUrls = [];

    const photosFromMessages = updates.result
        .filter(el => el.message.photo != undefined)
        .map(async (el) => {
            const photoMeta = await getPhotoMetadata(el.message.photo[2].file_id);
            const photoUrl = await getPhotoUrl(photoMeta.result.file_path);
            console.log(photoUrl);
            photoUrls.push(photoUrl);
            return photoUrl;
        });


    const messages = updates.result.reduce(function (acc, next) {
        acc += next.message.from.first_name + " " + ": " + next.message.text + "\n";
        return acc;
    }, "");

    const photoUrl = await getUserPhoto(updates.result[updates.result.length - 1].message.from.id)

    printMessages(messages);
    insertPhoto(photoUrl);

    insertPhotos(photosFromMessages);
}

async function getTelegramUpdates() {
    return $.getJSON({
        url: "https://api.telegram.org/bot" + telegramBotToken + "/getUpdates",
        jsonp: "callback",
        dataType: "json"
    }).promise();
}

function printMessages(text) {
    const div = document.getElementById('messages');

    div.innerText = text;
}

function insertPhoto(url) {
    const img = document.getElementById('photo');
    img.src = url;
}

function insertPhotos(urls) {
    const photos = document.getElementById('photos');

    const images = urls.map(el => {
        const listItem = document.createElement('li');
        img.src = el;
        listItem.appendChild(img);
        return listItem;
    });

    images.forEach(element => {
        photos.appendChild(element);
    });
}

async function getUserPhoto(userId) {
    const photos = await $.getJSON({
        url: "https://api.telegram.org/bot" + telegramBotToken + "/getUserProfilePhotos?user_id=" + userId,
        jsonp: "callback",
        dataType: "json"
    }).promise();


    const fileId = photos.result.photos[1][0].file_id;

    const fileResponse = await $.getJSON({
        url: "https://api.telegram.org/bot" + telegramBotToken + "/getFile?file_id=" + fileId,
        jsonp: "callback",
        dataType: "json"
    }).promise();

    return "https://api.telegram.org/file/bot" + telegramBotToken + "/" + fileResponse.result.file_path;
}

async function getPhotoMetadata(fileId) {
    return await $.getJSON({
        url: "https://api.telegram.org/bot" + telegramBotToken + "/getFile?file_id=" + fileId,
        jsonp: "callback",
        dataType: "json"
    }).promise();
}

async function getPhotoUrl(filePath) {
    return "https://api.telegram.org/file/bot" + telegramBotToken + "/" + filePath;
}

