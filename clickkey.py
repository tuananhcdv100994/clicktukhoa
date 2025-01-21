from playwright.sync_api import sync_playwright
import time
import random

def search_and_click(keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Sử dụng trình duyệt headless
        context = browser.new_context()
        page = context.new_page()

        # Truy cập Google
        page.goto("https://www.google.com")
        page.fill("input[name=q]", keyword)  # Điền từ khóa
        page.keyboard.press("Enter")
        time.sleep(3)  # Đợi kết quả tải

        # Click vào kết quả đầu tiên
        try:
            first_result = page.query_selector("div.g a")
            if first_result:
                first_result.click()
                print(f"Successfully clicked on the first result for: {keyword}")
                time.sleep(random.randint(15, 20))
            else:
                print("No clickable result found!")
        except Exception as e:
            print(f"Error clicking result: {e}")

        browser.close()

if __name__ == "__main__":
    keywords = ["màn hình crv", "màn hình android crv"]
    for keyword in keywords:
        search_and_click(keyword)
