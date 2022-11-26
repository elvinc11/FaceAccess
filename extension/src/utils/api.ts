export async function fetchBlockedWebsites(url: string): Promise<any> {
    const res = await fetch('http://127.0.0.1:8000/getAllBlockedWebsites');

    if (!res.ok){
        throw new Error('not found');
    }

    const data = await res.json();
    return data;
}