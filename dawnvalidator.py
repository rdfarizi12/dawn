import asyncio
import json
import aiohttp  # Ensure you have this library installed
from loguru import logger
import random  # Import random for random selection

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
    proxy_url = None  # Initialize proxy_url to avoid referencing before assignment
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
    appid = "66fea3b25af24c1ea7e8acee"  # Your app ID
    bearer_token = "2056b72d0eb33beb2a6d2d39c67296afa677fc1f271efaf0d84b5d50cd08aee410c07f2f8a6510b58ab067551517964a9b712a207a15ea4f311b2b0364b0fd4bae7648c4edd4df846361d141db0c35885277c641e0d6afbe952763136f733b572d940642f6a219d38dfdbc83fec35de354770e5ecae26f70015803c1e5788013a96dcd0456768d1dae2de7d2aa570f6b74eab39fc7cb62ca20c08cce93a60eb9ce86cb5993e174b9fe0757dfa2418dabde0a54bae454090db78abd37cb566930d2178cde8702b59ff7c548f8fa33070b577c87ea946b80723687eff8fb0a62c17beaed25971329056c18227337d1166d960fdb4473a474ccc711ff3c60b3cc23"  # Your bearer token
    username = "usergues.only@gmail.com"  # Replace with the actual username
    extension_id = "fpdkjdnhkakefebpekbdhillbhonfjjp"  # Replace with the actual extension ID
    number_of_tabs = 0  # Adjust this value if needed

    # Read proxies from proxy.txt
    proxies = await read_proxies_from_file("proxy.txt")
    
    if not proxies:
        logger.info("No proxies found in proxy.txt. Running without a proxy.")
        proxy = None
    else:
        logger.info(f"Using {len(proxies)} proxies.")
    
    while True:  # Auto loop
        logger.info("Join Grup https://t.me/dasarpemulung")
        proxy = random.choice(proxies) if proxies else None  # Randomly select a proxy if available
        logger.info(f"Using proxy: {proxy}")  # Log the selected proxy
        
        response = await send_keepalive_request(appid, bearer_token, username, extension_id, number_of_tabs, proxy)
        if response is None:
            logger.info("Channel Youtube Dasar Pemulung")
            logger.error("Failed to keep alive, retrying in 10 seconds...")
            await asyncio.sleep(5)  # Wait before retrying
        else:
            logger.info("Channel Youtube Dasar Pemulung")
            logger.info("Keep alive successful, waiting for the next cycle...")
            await asyncio.sleep(10)  # Wait for a specified interval before the next request

if __name__ == '__main__':
    asyncio.run(main())
