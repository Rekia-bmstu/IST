const ACCESS_TOKEN = "1e6fc5ae345b2af29028971a82627158b07cff065db6d25f57ed113ebf333135469fb4ff8004dc6a50da0";
let GROUPS_AS_STRING = '';

function getGroups() {
    const inputValue = document.getElementById('amount-input').value;
    const count = inputValue >= 1 ? inputValue : 5;

    $.getJSON({
        url: 'https://api.vk.com/method/groups.get?access_token=' + ACCESS_TOKEN + '&v=5.131&filter=publics&extended=1&fields=members_count&count=' + count,
        jsonp: "callback",
        dataType: "jsonp"
    }).done(function (data) {
        var groupsAsString = "";

        const items = data.response.items;

        const groups = [];
        for (let i = 0; i < items.length; i++) {
            groupsAsString += (i + 1) + ". " + items[i].name + " - " + items[i].members_count + "\n";
            groups.push((i + 1) + ". " + items[i].name + " - " + items[i].members_count);
        }

        GROUPS_AS_STRING = groupsAsString;

        console.log(groups);

        const groupsList = document.getElementById('groups-list');

        groups.forEach(element => {
            const listItem = document.createElement('li');
            listItem.innerHTML = element;
            groupsList.appendChild(listItem)
        });
        
        // $.getJSON({
        //     url: "https://api.vk.com/method/wall.post?access_token=" + ACCESS_TOKEN + "&v=5.131&owner_id=216462892&message=" + groups,
        //     jsonp: "callback",
        //     dataType: "jsonp"

        // }).done(function (data) {
        //     console.log(data);
        //     alert('PostId: ' + data.response.post_id);
        // });
    });
}

function send() {
    if (GROUPS_AS_STRING === '' || GROUPS_AS_STRING == undefined) {
        alert("данные не загружены");
        return;
    }

    alert("типо запостил");
    return;
    
    $.getJSON({
            url: "https://api.vk.com/method/wall.post?access_token=" + ACCESS_TOKEN + "&v=5.131&owner_id=216462892&message=" + groups,
            jsonp: "callback",
            dataType: "jsonp"

        }).done(function (data) {
            console.log(data);
            alert('PostId: ' + data.response.post_id);
        });
    
}