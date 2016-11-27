// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });

var API = "http://hackhate.huguesverlin.fr/";

//example of using a message handler from the inject scripts
chrome.extension.onMessage.addListener(
    function (request, sender, sendResponse) {
        chrome.pageAction.show(sender.tab.id);
        sendResponse();
    });


CallHackApi = function (word) {
    var bkg = chrome.extension.getBackgroundPage();
    var query = word.selectionText;

    chrome.tabs.create(
        {url: API + "analysis?text=" + query}
    );

};

GetPageUrl = function () {
    var bkg = chrome.extension.getBackgroundPage();
    bkg.console.log(window.location);

    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        var url = tabs[0].url;
        chrome.tabs.create(
            {url: API + "analysis?text=" + url}
        )
    });
};

chrome.contextMenus.create({
    title: "Hate Speech analysis",
    contexts: ["selection"],
    onclick: CallHackApi
});

chrome.contextMenus.create({
    title: "Hate analysis",
    contexts: ["page"],
    onclick: GetPageUrl
});