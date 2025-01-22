#!/usr/bin/env python3

import time
import random
import requests
from bs4 import BeautifulSoup

def get_free_proxies():
    """
    Lấy danh sách proxy miễn phí từ free-proxy-list.net.
    """
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    for row in soup.find("table", id="proxylisttable").find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) > 6 and cols[6].text == "yes":  # HTTPS proxy
            proxies.append(f"{cols[0].text}:{cols[1].text}")
    return proxies

def google_search(keyword, proxy=None):
    """
    Tìm kiếm từ khóa trên Google và trả về danh sách các kết quả.
    """
    try:
        base_url = "https://www.google.com/search"
        params = {'q': keyword}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Ubuntu; rv:110.0) Gecko/20100101 Firefox/110.0'
        }
        proxies = {"https": proxy} if proxy else None
        
        response = requests.get(base_url, params=params, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if "/url?q=" in link:
                actual_link = link.split("/url?q=")[1].split("&")[0]
                search_results.append(actual_link)
        
        return search_results
    except Exception as e:
        print(f"Lỗi khi tìm kiếm Google: {e}")
        return []

def click_link(url, proxy=None):
    """
    Giả lập click vào liên kết bằng cách gửi request qua proxy.
    """
    try:
        proxies = {"https": proxy} if proxy else None
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, proxies=proxies, timeout=10)
        response.raise_for_status()
        print(f"Đã click liên kết: {url}")
        return True
    except Exception as e:
        print(f"Lỗi khi click liên kết: {e}")
        return False

def main():
    # Nhập danh sách từ khóa và domain cần kiểm tra
    keywords = input("Nhập danh sách từ khóa (cách nhau bằng dấu phẩy): ").split(',')
    keywords = [kw.strip() for kw in keywords]
    target_domain = input("Nhập domain cần click (ví dụ: example.com): ").strip()
    
    # Lấy danh sách proxy miễn phí
    print("Đang tải proxy miễn phí...")
    proxies = get_free_proxies()
    print(f"Tìm thấy {len(proxies)} proxy.")
    
    while True:  # Vòng lặp liên tục
        for keyword in keywords:
            print(f"Tìm kiếm từ khóa: {keyword}")
            proxy = random.choice(proxies) if proxies else None
            print(f"Sử dụng proxy: {proxy}")
            
            results = google_search(keyword, proxy)
            if not results:
                print(f"Không tìm thấy kết quả nào cho từ khóa '{keyword}'.")
                continue
            
            clicked = False
            for result in results:
                if target_domain in result:
                    print(f"Đã tìm thấy liên kết phù hợp: {result}")
                    if click_link(result, proxy):
                        print(f"Đã click từ khóa '{keyword}'.")
                        clicked = True
                    break
            
            if not clicked:
                print(f"Không tìm thấy kết quả nào phù hợp với domain '{target_domain}' cho từ khóa '{keyword}'.")
            
            # Thời gian chờ ngẫu nhiên từ 5 đến 15 giây
            wait_time = random.randint(5, 15)
            print(f"Đợi {wait_time} giây trước khi tiếp tục...")
            time.sleep(wait_time)
        
        print("Hoàn thành một vòng lặp. Tiếp tục vòng lặp mới sau 30 giây...")
        time.sleep(30)

if __name__ == "__main__":
    main()
