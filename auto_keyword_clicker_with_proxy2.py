#!/usr/bin/env python3

import time
import random
import requests
from bs4 import BeautifulSoup

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
        
        # In nội dung HTML trả về để kiểm tra
        print(f"Debug HTML trả về cho từ khóa '{keyword}':\n")
        print(response.text[:1000])  # Chỉ in 1000 ký tự đầu để tránh quá dài
        
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        # Kiểm tra cấu trúc HTML
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if "/url?q=" in link:
                actual_link = link.split("/url?q=")[1].split("&")[0]
                search_results.append(actual_link)
        
        return search_results
    except Exception as e:
        print(f"Lỗi khi tìm kiếm Google: {e}")
        return []

def main():
    keywords = input("Nhập danh sách từ khóa (cách nhau bằng dấu phẩy): ").split(',')
    keywords = [kw.strip() for kw in keywords]
    target_domain = input("Nhập domain cần click (ví dụ: example.com): ").strip()
    
    while True:
        for keyword in keywords:
            print(f"Tìm kiếm từ khóa: {keyword}")
            results = google_search(keyword)
            if not results:
                print(f"Không tìm thấy kết quả nào cho từ khóa '{keyword}'.")
                continue
            
            # Kiểm tra và click vào kết quả chứa domain yêu cầu
            clicked = False
            for result in results:
                if target_domain in result:
                    print(f"Đã tìm thấy liên kết phù hợp: {result}")
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
