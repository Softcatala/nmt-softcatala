
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
    url = `http://localhost:8700/version/`;

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
    url = `http://localhost:8700/translate/?text=${text}`;

    var client = new HttpClient();
    client.get(url, function(response) {
        json = JSON.parse(response);
        element = document.getElementById('translated_text');
        text = json["translated"];
        element.innerText = text;

        element = document.getElementById('time_used');
        text = json["time"];
        element.innerText = text;
    });
}

