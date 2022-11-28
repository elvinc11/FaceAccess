
export interface LocalStorage {
  url?: string[]
}

export type LocalStorageKeys = keyof LocalStorage

export function setStoredUrls(url: string[]): Promise<void> {
  const vals: LocalStorage = {
    url,
  }
  return new Promise((resolve) => {
    chrome.storage.local.set(vals, () => {
      resolve()
    })
  })
}

export function getStoredUrls(): Promise<string[]> {
  const keys: LocalStorageKeys[] = ['url']
  return new Promise((resolve) => {
    chrome.storage.local.get(keys, (res: LocalStorage) => {
      resolve(res.url ?? [])
    })
  })
}

