var DO_NOT_LOG_TAG = "DO_NOT_LOG";

function addXMLRequestCallback(callback){
    var oldSend, oldOpen;

    // create a callback queue
    XMLHttpRequest.callback = callback;
    // store the native send()
    oldSend = XMLHttpRequest.prototype.send;
    oldOpen = XMLHttpRequest.prototype.open;
    // override the native send()
    XMLHttpRequest.prototype.send = function(){
        // process the callback queue
        // the xhr instance is passed into each callback but seems pretty useless
        // you can't tell what its destination is or call abort() without an error
        // so only really good for logging that a request has happened
        // I could be wrong, I hope so...
        // EDIT: I suppose you could override the onreadystatechange handler though
        
        XMLHttpRequest.callback( "send", this, arguments );
        
        // call the native send()
        oldSend.apply(this, arguments);
    }
    XMLHttpRequest.prototype.open = function() {
        XMLHttpRequest.callback( "open", this, arguments );
        oldOpen.apply(this, arguments);        
    }
}

function logMsg(msg) {
        document.getElementById('log').innerHTML += msg;
        document.getElementById('log').innerHTML += "\n";
}

function logRemote(method, path, data) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, g_opt.base + url, true);
        xhr.send(data);
}

addXMLRequestCallback(function(fnct, self, args) {
    logMsg(fnct + " -- " + JSON.prune(args));
});