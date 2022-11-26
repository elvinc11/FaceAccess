chrome.runtime.sendMessage('from the content script', (response) => {
    console.log(response)
} )