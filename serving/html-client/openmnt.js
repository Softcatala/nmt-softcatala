
// https://www.softcatala.org/sc/v2/api/nmt-engcat/
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

function change_direction() {
    
    element = document.getElementById('languages');
    element_action = document.getElementById('change_language');
    languages = element.value;
    
    if (languages == 'eng-cat') {
        languages = 'cat-eng';
        action_text = 'Direcció català - anglès';
    }
    else {
        languages = 'eng-cat';
        action_text = 'Direcció actual anglès - català';
    }

    element.value = languages
    element_action.value = action_text
}

function translate_text() {

    text = document.getElementById('source_text').value;
    languages = document.getElementById('languages').value;
    url = URL + `/translate/?text=${text}&languages=${languages}`;

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

