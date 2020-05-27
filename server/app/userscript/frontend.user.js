// ==UserScript==
// @name     Usertagger
// @version  1
// @include  http://*.reddit.com/*
// @include  http://reddit.com/*
// @include  https://*.reddit.com/*
// @include  https://reddit.com/*
// @grant    GM.xmlHttpRequest
// @namespace __BASEURL__
// ==/UserScript==

let requestURL = '__BASEURL__/bulk_users';
let re = "https?:\/\/(?:.*\.)?reddit.com\/u(?:ser)?\/(.*)"

function massRequestUsername(usernames, callback) {
    let url = new URL(requestURL);

    usernames.forEach(function(username) {
        url.searchParams.append('usernames', username)
    });

    GM.xmlHttpRequest({
        method: "GET",
        url: url,
        onload: callback
    });
}

function getAllAuthorsFromPage() {
	let usernames = []
    document.querySelectorAll(".author").forEach(function(node) {
        let username = node.href.match(re)

        if(usernames.indexOf(username) === -1) {
            usernames.push(username[1]);
        }
	});
    return usernames
}

function injectAfterAllAuthorsFromPage(responseJSON) {
    document.querySelectorAll(".author").forEach(function(node) {
        let username = node.href.match(re);

        var el = document.createElement("span");    
        el.innerHTML = responseJSON[username[1]];
        console.log(el);
        node.parentNode.insertBefore(el, node.nextSibling);
  });  
}

function main() {
    let usernames = getAllAuthorsFromPage()
    massRequestUsername(usernames, function(response) {
        injectAfterAllAuthorsFromPage(JSON.parse(response.responseText).results);
    });
}

main();