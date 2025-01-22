#!/usr/bin/env python3

import time
import requests
from bs4 import BeautifulSoup

def google_search(keyword):
    """
    Tìm kiếm từ khóa trên Google và trả về danh sách các kết quả.
    """
    try:
        base_url = "https://www.google.com/search"
        params = {'q': keyword}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Ubuntu; rv:110.0) Gecko/20100101 Firefox/110.0'
        }
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        # Tìm tất cả các liên kết trong kết quả tìm kiếm
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            # Lọc chỉ các liên kết thực (bỏ qua liên kết không cần thiết của Google)
            if "/url?q=" in link:
                actual_link = link.split("/url?q=")[1].split("&")[0]
                search_results.append(actual_link)
        
        return search_results
    except Exception as e:
        print(f"Lỗi khi tìm kiếm Google: {e}")
        return []

def click_link(url):
    """
    Giả lập click vào liên kết bằng cách gửi request.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
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
    
    while True:  # Vòng lặp liên tục
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
                    if click_link(result):
                        print(f"Đã click từ khóa '{keyword}'.")
                        clicked = True
                    break
            
            if not clicked:
                print(f"Không tìm thấy kết quả nào phù hợp với domain '{target_domain}' cho từ khóa '{keyword}'.")
            
            # Đợi trước khi tìm kiếm từ khóa tiếp theo (tránh bị chặn bởi Google)
            time.sleep(2)
        
        print("Hoàn thành một vòng lặp. Tiếp tục vòng lặp mới sau 10 giây...")
        time.sleep(10)

if __name__ == "__main__":
    main()
