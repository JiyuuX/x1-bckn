import requests
from requests.exceptions import RequestException

def get_instagram_data(username):
    # Proxy ayarlarını yapılandırın
    proxy = 'http://your_proxy_address:port'  # Örnek: 'http://123.456.789.0:8080'
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    
    # İstek başlıklarını yapılandırın
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': 'ig_did=0513863C-41F1-47BF-B2BA-8432258316B6; ...',  # Cookie değerlerinizi buraya ekleyin
    }
    
    try:
        # Instagram API isteği URL'si
        url = f"https://www.instagram.com/{username}/?__a=1"
        response = requests.get(url, headers=headers, proxies=proxies, verify=False)
        response.raise_for_status()  # Hata varsa istisna fırlatır
        user_data = response.json()
        user_id = user_data['graphql']['user']['id']
        return user_id
    except RequestException as e:
        print("Error fetching user ID from Instagram:", e)
        return None

# Örnek kullanıcı adı
username = 'japaneseammo_misa'
user_id = get_instagram_data(username)
print(f"User ID: {user_id}")
