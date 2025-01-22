#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_keywords(url):
    """
    Trích xuất từ khóa từ website.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and 'content' in meta_keywords.attrs:
            keywords = meta_keywords['content'].split(',')
            return [kw.strip() for kw in keywords]
        else:
            print("Không tìm thấy meta keywords.")
            return []
    except Exception as e:
        print(f"Lỗi khi trích xuất từ khóa: {e}")
        return []

def google_search(keyword):
    """
    Tìm kiếm từ khóa trên Google và trả về kết quả đầu tiên.
    """
    try:
        base_url = "https://www.google.com/search"
        params = {'q': keyword}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Ubuntu; rv:110.0) Gecko/20100101 Firefox/110.0'
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm kết quả đầu tiên
        result = soup.find('a', href=True)
        if result:
            return urllib.parse.urljoin(base_url, result['href'])
        else:
            print(f"Không tìm thấy kết quả nào cho từ khóa: {keyword}")
            return None
    except Exception as e:
        print(f"Lỗi khi tìm kiếm Google: {e}")
        return None

def main():
    # Nhập URL website
    website_url = input("Nhập URL website: ").strip()
    
    # Trích xuất từ khóa từ website
    keywords = extract_keywords(website_url)
    if not keywords:
        print("Không có từ khóa nào để tìm kiếm.")
        return
    
    print(f"Tìm thấy từ khóa: {keywords}")
    
    # Tìm kiếm từng từ khóa trên Google
    for keyword in keywords:
        print(f"Tìm kiếm từ khóa: {keyword}")
        result_url = google_search(keyword)
        if result_url:
            print(f"Kết quả đầu tiên cho từ khóa '{keyword}': {result_url}")
        else:
            print(f"Không tìm thấy kết quả cho từ khóa '{keyword}'.")

if __name__ == "__main__":
    main()
