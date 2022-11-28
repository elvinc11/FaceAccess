
export interface WebsiteData {
    website_id: Number;
    url: string;
    [key: string]: any;
}


export async function fetchBlockedWebsites(): Promise<WebsiteData[]> {
    const res = await fetch('http://127.0.0.1:8000/getWebsites');

    if (!res.ok){
        throw new Error('not found');
    }

    const data: WebsiteData[] = await res.json();
    return data;
}