const ACCESS_TOKEN = "1e6fc5ae345b2af29028971a82627158b07cff065db6d25f57ed113ebf333135469fb4ff8004dc6a50da0";
const REQUEST_URL = 'https://api.vk.com/method/friends.get?access_token=' + ACCESS_TOKEN + '&v=5.131&fields=nickname,sex,education';
const USER_ID = "216462892";

console.log(USER_ID);
$.getJSON({
    url: REQUEST_URL,
    jsonp: "callback",
    dataType: "jsonp"
}).done(function(data) {
    console.log(data.response.items);
    fillTable(data.response.items);
});

function fillTable(data) {
    const tableBody = document.getElementById('friends-table').getElementsByTagName('tbody')[0];

    for(var i = 0; i < data.length; i++) {
        const e = data[i];

        const tableRow = document.createElement('tr');
        
        var tableData = document.createElement('td');
        tableData.innerHTML = i + 1;
        tableRow.appendChild(tableData);

        var tableData = document.createElement('td'); 
        tableData.innerHTML = e.id;
        tableRow.appendChild(tableData);

        tableData = document.createElement('td');
        tableData.innerHTML = e.first_name + ' ' + e.last_name;
        tableRow.appendChild(tableData);

        tableData = document.createElement('td');
        tableData.innerHTML = e.sex == 1 ? "Женский" : "Мужской";
        tableRow.appendChild(tableData);

        tableData = document.createElement('td');
        tableData.innerHTML = e.university_name ?? "";
        tableRow.appendChild(tableData);

        tableBody.appendChild(tableRow);
    }
}

function fact(n) {
    if (n == 1)
        return n;

    return n * fact(n - 1);
}

function main(expr, n) {
    return expr(n);
}

console.log((main(fact, 5)));