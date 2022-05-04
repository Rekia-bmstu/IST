const ACCESS_TOKEN = "58a010ee6f3f595e848051bbff4eebdc084281f1d4135e404e6712af89106bd882307b8b0147aa28c5f73";

function buttonClicked() {
    const ownerId = document.getElementById('owner_id').value;
    const postId = document.getElementById('post_id').value;

    const requestUrl = 'https://api.vk.com/method/wall.createComment?access_token=' + ACCESS_TOKEN + '&v=5.131&owner_id=' + ownerId + '&post_id=' + postId + '&message=test';

    console.log(requestUrl);
    $.getJSON({
        url: requestUrl,
        jsonp: "callback",
        dataType: "jsonp"
    }).done(function(data) {
        console.log(data);
    });
}  