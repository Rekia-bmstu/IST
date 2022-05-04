const ACCESS_TOKEN = "1e6fc5ae345b2af29028971a82627158b07cff065db6d25f57ed113ebf333135469fb4ff8004dc6a50da0";

async function postGroups() {
    const inputValue = document.getElementById('amount-input').value;
    const count = inputValue >= 1 ? inputValue : 5;

    const groupsResponse = await getMyGroups(count);
    const postText = formatGroupsResponse(groupsResponse);
    const makePostResponse = await makePost(postText);
    console.log(makePostResponse);
    alert('PostId: ' + makePostResponse.response.post_id);
}

async function getMyGroups(count) {
    return $.getJSON({
        url: 'https://api.vk.com/method/groups.get?access_token=' + ACCESS_TOKEN + '&v=5.131&filter=publics&extended=1&fields=members_count&count=' + count,
        jsonp: "callback",
        dataType: "jsonp"
    }).promise();
}

async function makePost(message) {
    return $.getJSON({
        url: "https://api.vk.com/method/wall.post?access_token=" + ACCESS_TOKEN + "&v=5.131&owner_id=216462892&message=" + message,
        jsonp: "callback",
        dataType: "jsonp"
    
    }).promise();
}

function formatGroupsResponse(data) {
    var groups = "";
    
    const items = data.response.items;

    for(var i = 0; i < items.length; i++)
        groups += (i + 1) + ". " + items[i].name + " - " + items[i].members_count + "%0A";

    return groups;
}