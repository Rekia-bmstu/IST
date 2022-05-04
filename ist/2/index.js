const STUDENT_ROWS = ["name", "group"];
const REQUEST_ROWS = ["theme", "header", "emergency-rate", "request-date"];

function loadRequests() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'Requests.xml', false);
    xhr.send();

    return xhr.responseXML;
}

function addRequest(data, requestNumber) {
    const requests = data.getElementsByTagName('request');

    const tableBody = document.getElementById('requests-table').getElementsByTagName('tbody')[0];
    const tableRow = document.createElement('tr');

    const numElem = document.createElement('td');
    numElem.innerHTML = requestNumber;
    tableRow.appendChild(numElem);

    const request = requests[requestNumber - 1];
    const user = request.getElementsByTagName("user")[0];
    const requestDetails = request.getElementsByTagName("request-details")[0];

    STUDENT_ROWS.forEach(tagName => {
        const td = document.createElement('td');
        td.innerHTML = user.getElementsByTagName(tagName)[0].innerHTML;
        tableRow.appendChild(td);
    });

    REQUEST_ROWS.forEach(tagName => {
        const td = document.createElement('td');
        td.innerHTML = requestDetails.getElementsByTagName(tagName)[0].innerHTML;
        console.log(td.innerHTML);
        tableRow.appendChild(td);
    })

    tableBody.appendChild(tableRow);
}

function addAllRequests(data) {
    const requestsAmount = data.getElementsByTagName('request').length;

    for(var i = 0; i < requestsAmount; i++)
        addRequest(xmlData, i + 1);
}

function clearTableBody() {
    const tableBody = document.getElementById('requests-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
}

function getRequestButtonClicked() {
    const requestsAmount = xmlData.getElementsByTagName('request').length;
    const requestNum = Number(document.getElementById('request-input').value);

    clearTableBody();

    if (requestNum == 0)
        addAllRequests(xmlData);
    else
        addRequest(xmlData, requestNum);
    
}

const xmlData = loadRequests();