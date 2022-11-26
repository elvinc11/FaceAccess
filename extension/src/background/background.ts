chrome.runtime.onMessage.addListener((msg, sender, SendReponse) => {
    console.log(msg)
    console.log(sender)
    SendReponse('from the background script!')
})