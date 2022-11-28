import { setStoredUrls } from "../utils/storage";

chrome.runtime.onInstalled.addListener(() => {
    setStoredUrls([])
})
