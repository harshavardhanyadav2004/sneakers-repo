import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
import json

class SimpleKickscrewScraper:
    def __init__(self):
        self.base_url = "https://www.kickscrew.com"
        self.categories = {
            'air-jordan': 'Air Jordan',
            'nike': 'Nike',
            'adidas': 'Adidas',
            'adidas-yeezy': 'Yeezy',
            'new-balance': 'New Balance',
            'asics': 'Asics',
            'onitsuka-tiger': 'Onitsuka Tiger'
        }
        self.products_data = []
        self.scraperapi_key = 'de2d92fc4b496279defa0f951aba2b0e'  # <-- Replace with your actual key

    def extract_sku_from_url(self, product_url):
        if not product_url or '/products/' not in product_url:
            return None
        url_path = product_url.split('/')[-1]
        sku_match = re.search(r'([a-z0-9]+-[0-9]+)(?:-.*)?$', url_path, re.IGNORECASE)
        if sku_match:
            return sku_match.group(1).lower()
        patterns = re.findall(r'[a-z]+[0-9]+-[0-9]+', url_path, re.IGNORECASE)
        if patterns:
            return patterns[-1].lower()
        return re.sub(r'[^a-z0-9-]', '', url_path.lower())

    def get_page_content(self, url, max_retries=3):
        scraperapi_url = "http://api.scraperapi.com/"
        params = {
            'api_key': self.scraperapi_key,
            'url': url,
            'render': 'false'
        }

        for attempt in range(max_retries):
            try:
                print(f"Fetching (via ScraperAPI): {url} (attempt {attempt + 1})")
                response = requests.get(scraperapi_url, params=params, timeout=15)
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 403:
                    print(f"Access denied (403) for {url}")
                    return None
                elif response.status_code == 404:
                    print(f"Page not found (404) for {url}")
                    return None
                else:
                    print(f"HTTP {response.status_code} for {url}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(2, 5) * (attempt + 1)
                print(f"Waiting {wait_time:.1f}s before retry...")
                time.sleep(wait_time)
        return None

    def extract_products_from_html(self, html_content, category_name, page_url):
        if not html_content:
            return []
        soup = BeautifulSoup(html_content, 'html.parser')
        products = []
        product_links = soup.find_all('a', href=re.compile(r'/products/'))

        for link in product_links:
            try:
                href = link.get('href')
                if not href:
                    continue
                product_url = self.base_url + href if href.startswith('/') else href
                product_data = self.extract_product_info_from_link(link, product_url, category_name)
                if product_data:
                    products.append(product_data)
            except Exception:
                continue

        if not products:
            products = self.extract_from_json_ld(soup, category_name)

        if not products:
            products = self.extract_from_ecommerce_patterns(soup, category_name, page_url)

        unique_products = []
        seen_ids = set()
        for product in products:
            if product['product_id'] not in seen_ids:
                seen_ids.add(product['product_id'])
                unique_products.append(product)
        return unique_products

    def extract_product_info_from_link(self, link_element, product_url, category_name):
        try:
            product_id = self.extract_sku_from_url(product_url)
            if not product_id:
                return None
            product_name = ""
            title = link_element.get('title', '').strip()
            if title and len(title) > 5:
                product_name = title
            if not product_name:
                img = link_element.find('img')
                if img:
                    alt = img.get('alt', '').strip()
                    if alt and len(alt) > 5:
                        product_name = alt
            if not product_name:
                text = link_element.get_text(strip=True)
                if text and len(text) > 5 and len(text) < 100:
                    product_name = text
            if not product_name and link_element.parent:
                parent_text = link_element.parent.get_text(strip=True)
                if parent_text and len(parent_text) > 5 and len(parent_text) < 100:
                    link_text = link_element.get_text(strip=True)
                    if link_text:
                        parent_text = parent_text.replace(link_text, '').strip()
                    if parent_text:
                        product_name = parent_text
            image_url = ""
            img = link_element.find('img')
            if img:
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if src:
                    image_url = self.base_url + src if src.startswith('/') else src
            if product_name:
                product_name = re.sub(r'\s+', ' ', product_name).strip()
                product_name = re.sub(r'^(Image of|Photo of|Picture of)\s+', '', product_name, flags=re.IGNORECASE)
            if product_name and product_id:
                return {
                    'category': category_name,
                    'style_name': product_name,
                    'product_id': product_id,
                    'url': product_url,
                    'image_url': image_url
                }
        except Exception:
            pass
        return None

    def extract_from_json_ld(self, soup, category_name):
        products = []
        try:
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        for item in data:
                            product = self.parse_json_ld_item(item, category_name)
                            if product:
                                products.append(product)
                    else:
                        product = self.parse_json_ld_item(data, category_name)
                        if product:
                            products.append(product)
                except json.JSONDecodeError:
                    continue
        except Exception:
            pass
        return products

    def parse_json_ld_item(self, item, category_name):
        try:
            if item.get('@type') == 'Product':
                name = item.get('name', '')
                url = item.get('url', '')
                image = item.get('image', '')
                if isinstance(image, list) and image:
                    image = image[0]
                if name and url and '/products/' in url:
                    product_id = self.extract_sku_from_url(url)
                    if product_id:
                        return {
                            'category': category_name,
                            'style_name': name,
                            'product_id': product_id,
                            'url': url if url.startswith('http') else self.base_url + url,
                            'image_url': image if image.startswith('http') else self.base_url + image if image else ''
                        }
        except Exception:
            pass
        return None

    def extract_from_ecommerce_patterns(self, soup, category_name, page_url):
        products = []
        selectors = ['.product-item', '.grid-item', '.product', '[class*="product"]', '.card', '[data-product]', '.item']
        for selector in selectors:
            try:
                containers = soup.select(selector)
                if containers:
                    for container in containers:
                        link = container.find('a', href=re.compile(r'/products/'))
                        if link:
                            href = link.get('href')
                            if href:
                                product_url = self.base_url + href if href.startswith('/') else href
                                product_data = self.extract_product_info_from_link(link, product_url, category_name)
                                if product_data:
                                    products.append(product_data)
                    if products:
                        break
            except Exception:
                continue
        return products

    def scrape_category(self, category_slug, category_name):
        print(f"\nScraping category: {category_name}")
        all_products = []
        page = 1
        while True:
            urls_to_try = [
                f"{self.base_url}/collections/{category_slug}?page={page}",
                f"{self.base_url}/collections/{category_slug}?p={page}",
                f"{self.base_url}/collections/{category_slug}" + (f"/{page}" if page > 1 else ""),
            ]
            page_products = []
            for url in urls_to_try:
                html_content = self.get_page_content(url)
                if html_content:
                    page_products = self.extract_products_from_html(html_content, category_name, url)
                    if page_products:
                        print(f"Found {len(page_products)} products")
                        break
                time.sleep(random.uniform(1, 3))
            if not page_products:
                print("No more products found.")
                break
            all_products.extend(page_products)
            if len(page_products) < 10:
                break
            page += 1
            if page > 20:
                break
            time.sleep(random.uniform(3, 6))
        return all_products

    def scrape_all_categories(self):
        print("Starting Kickscrew Scraper")
        for slug, name in self.categories.items():
            category_products = self.scrape_category(slug, name)
            self.products_data.extend(category_products)
            if slug != list(self.categories.keys())[-1]:
                time.sleep(random.uniform(5, 10))
        return self.products_data

    def save_to_csv(self, filename='kickscrew_products_simple.csv'):
        if not self.products_data:
            print("No data to save.")
            return
        df = pd.DataFrame(self.products_data).drop_duplicates(subset=['product_id'])
        df.to_csv(filename, index=False)
        print(f"\nSaved {len(df)} unique products to {filename}")
        return df

    def run_scraper(self):
        products = self.scrape_all_categories()
        self.save_to_csv()
        return products

# --- Usage ---
if __name__ == "__main__":
    scraper = SimpleKickscrewScraper()
    products = scraper.run_scraper()
    if products:
        print(f"Scraped {len(products)} products")
    else:
        print("No products were scraped.")
