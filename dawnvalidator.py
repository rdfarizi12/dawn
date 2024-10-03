import asyncio
import json
import aiohttp  # Ensure you have this library installed
from loguru import logger

async def send_keepalive_request(appid, bearer_token, username, extension_id, number_of_tabs, proxy=None):
    url = f"https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive?appid={appid}"
    
    # Set headers with dynamic Origin based on extension_id
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": f"chrome-extension://{extension_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }
    
    payload = {
        "username": username,
        "extensionid": extension_id,
        "numberoftabs": number_of_tabs,
        "_v": "1.0.9"
    }

    connector = None
    if proxy:
        connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification for the proxy
        proxy_url = proxy if proxy.startswith('http://') or proxy.startswith('https://') else f"http://{proxy}"
    
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.post(url, headers=headers, json=payload, proxy=proxy_url) as response:
                response_data = await response.json()
                logger.info(f"Response: {response_data}")
                return response_data
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return None  # Return None in case of an error

async def read_proxies_from_file(file_path):
    """Read proxies from the specified file."""
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except FileNotFoundError:
        logger.error("Proxy file not found.")
        return []

async def main():
    appid = "CHANGE YOUR APP ID"  # Your app ID
    bearer_token = "CHANGE YOUR BEARER"  # Your bearer token
    username = "CHANGE YOUR EMAIL"  # Replace with the actual username
    extension_id = "CHANGE YOUR EXTENSION ID"  # Replace with the actual extension ID
    number_of_tabs = 0  # Adjust this value if needed

    # Read proxies from proxy.txt
    proxies = await read_proxies_from_file("proxy.txt")
    
    if not proxies:
        logger.info("No proxies found in proxy.txt. Running without a proxy.")
        proxy = None
    else:
        proxy = proxies[0]  # Use the first proxy from the list
        logger.info(f"Using proxy: {proxy}")

    while True:  # Auto loop
        response = await send_keepalive_request(appid, bearer_token, username, extension_id, number_of_tabs, proxy)
        if response is None:
            logger.error("Failed to keep alive, retrying in 10 seconds...")
            await asyncio.sleep(10)  # Wait before retrying
        else:
            logger.info("Keep alive successful, waiting for the next cycle...")
            await asyncio.sleep(30)  # Wait for a specified interval before the next request

if __name__ == '__main__':
    asyncio.run(main())
