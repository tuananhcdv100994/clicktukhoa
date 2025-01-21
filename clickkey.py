from playwright.sync_api import sync_playwright
import time
import random

def search_and_click(keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()

        # Truy cập Google
        page.goto("https://www.google.com")
        
        # Chờ selector xuất hiện
        try:
            page.wait_for_selector("input[name=q]", timeout=60000)  # Đợi 60 giây
            page.fill("input[name=q]", keyword)  # Điền từ khóa
            page.keyboard.press("Enter")  # Nhấn Enter
            time.sleep(3)  # Đợi kết quả tải

            # Click vào kết quả đầu tiên
            first_result = page.query_selector("div.g a")
            if first_result:
                first_result.click()
                print(f"Successfully clicked on the first result for: {keyword}")
                time.sleep(random.randint(15, 20))
            else:
                print("No clickable result found!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    keywords = ["màn hình crv", "màn hình android crv"]
    for keyword in keywords:
        search_and_click(keyword)
