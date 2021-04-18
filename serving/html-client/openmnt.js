
// https://www.softcatala.org/sc/v2/api/nmt-engcat
var URL='http://localhost:8700'

var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );
        anHttpRequest.send( null );
    }
}

function show_version() {
    url = URL + `/version/`;

    var client = new HttpClient();
    client.get(url, function(response) {
        json = JSON.parse(response);

        element = document.getElementById('version');
        var text = JSON.stringify(json);
        element.innerText = text;
    });
}

function translate_text() {

    text = document.getElementById('source_text').value;
    languages = document.getElementById('languages').value;

    var xhr = new XMLHttpRequest();
    url = URL + `/translate/`;
    xhr.open('POST', url);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            json = JSON.parse(xhr.responseText);
            element = document.getElementById('translated_text');
            text = json["responseData"]["translatedText"];
            element.value = text;

            element = document.getElementById('time_used');
            text = json["time"];
            element.innerText = text;

            element = document.getElementById('message');
            text = json["message"];
            if (typeof text == 'undefined') text = ""
            element.innerText = text;

        }
    }

    var payload = new FormData();
    payload.append('langpair', languages);
    payload.append('q', text);
    xhr.send(payload);
}


function sendFile()
{
    var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function()
        {
            if(xmlHttp.readyState != 4)
            {
                return;
            }

            if (xmlHttp.status == 200)
            {
                alert("D'aquí a una estona rebreu el fitxer traduït per correu electrònic");
            }
            else
            {
                json = JSON.parse(xmlHttp.responseText);
                alert(json['error']);
            }
        }

        var formData = new FormData(document.getElementById('form-id'));
        url = URL + `/translate_file/`;
        xmlHttp.open("post", url);
        xmlHttp.send(formData); 
}
