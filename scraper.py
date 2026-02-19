from playwright.sync_api import sync_playwright

def get_product_info(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)

            title = page.locator("h1").first.inner_text()
            paragraphs = page.locator("p").all_text_contents()
            description = " ".join(paragraphs[:5])

            bullets = page.locator("li").all_text_contents()
            bullet_points = bullets[:5]

            image = page.locator("img").first.get_attribute("src")

            browser.close()

            return {
                "title": title,
                "description": description,
                "bullet_points": bullet_points,
                "image_url": image
            }

    except Exception as e:
        print("Scraping failed for URL:", url, e)
        return None
