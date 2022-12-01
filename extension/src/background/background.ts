import {fetchBlockedWebsites} from '../utils/api';
let urls = [];

chrome.tabs.onUpdated.addListener ((tabId: number, changeInfo: chrome.tabs.TabChangeInfo, tab: chrome.tabs.Tab) => {
   
        if (changeInfo.url){
            fetchBlockedWebsites().then(data=>{
                data.forEach( website => {
                    urls.push(website.url);
                })
            }).catch(error=>{
                console.log(error);
            })
        }  
        chrome.runtime.onMessage.addListener((message, sender, sendReponse)=>{
            console.log(message);
            console.log(sender);
            sendReponse('from background');
            chrome.tabs.sendMessage(sender.tab.id, urls);
          })
    }
)

urls = [];



