from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
from urllib.parse import urlparse
from db_connection import insert_data  # Import the function to insert data into MongoDB

chrome_driver_path = "chromedriver.exe"
service = Service(chrome_driver_path)

# Add options to disable SSL certificate errors and other flags
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-software-rasterizer")  
chrome_options.add_argument("--log-level=3")  
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to retry loading a page
def retry_load(driver, url, retries=3):
    for i in range(retries):
        try:
            driver.get(url)
            return
        except Exception as e:
            print(f"Retry {i+1}/{retries} failed: {e}")
            time.sleep(5)  # wait before retrying
    raise Exception(f"Failed to load {url} after {retries} retries")

# Add random delay to avoid detection
time.sleep(random.uniform(2, 5))

# Create a list to store all articles
articles_data = []

try:
    retry_load(driver, "https://www.nbcbayarea.com/news/local/east-bay/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "site-content"))
    )
    
    ### FEATURED ARTICLE ###
    try:
        featured_article = driver.find_element(By.CLASS_NAME, "category-hero-item--primary-container")
        featured_title = featured_article.find_element(By.CSS_SELECTOR, "h3.story-card__title.more-news__story-card-title").text
        featured_url = featured_article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        # Visit the featured article URL
        retry_load(driver, featured_url)

        # Extract body text, publication date, and source domain
        body_text = " ".join([p.text for p in driver.find_elements(By.TAG_NAME, "p")])
        try:
            publication_date = driver.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
        except:
            publication_date = "Not Available"
        
        # Extract source domain from URL
        source_domain = urlparse(driver.current_url).netloc

        # Store the featured article data
        articles_data.append({
            "Title": featured_title,
            "Body Text": body_text,
            "Publication Date": publication_date,
            "Source Domain": source_domain,
            "URL": featured_url
        })

        # Return to main page
        driver.back()
        time.sleep(random.uniform(2, 4))
    
    except Exception as e:
        print(f"Error extracting featured article: {e}")
    
    ### TRENDING ARTICLES ###
    try:
        secondary_container = driver.find_element(By.CLASS_NAME, 'category-hero-item--secondary-container')
        story_list_sections = secondary_container.find_elements(By.CLASS_NAME, 'story-card__list-item')

        for section in story_list_sections:
            try:
                # Extract title and URL
                title = section.find_element(By.CSS_SELECTOR, 'h3.story-card__title.more-news__story-card-title').text
                url = section.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
                
                # Visit each article URL
                retry_load(driver, url)

                # Extract body text, publication date, and source domain
                body_text = " ".join([p.text for p in driver.find_elements(By.TAG_NAME, "p")])
                try:
                    publication_date = driver.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
                except:
                    publication_date = "Not Available"
                
                source_domain = urlparse(driver.current_url).netloc

                # Store the article data
                articles_data.append({
                    "Title": title,
                    "Body Text": body_text,
                    "Publication Date": publication_date,
                    "Source Domain": source_domain,
                    "URL": url
                })

                # Return to the main page
                driver.back()
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"Error processing article: {e}")
    except Exception as e:
        print(f"Error finding secondary container: {e}")

    ### SECONDARY MOBILE SECTION (Most Popular) ###
    try:
        secondary_mobile_section = driver.find_element(By.CLASS_NAME, 'section-content--secondary')
        most_popular_list = secondary_mobile_section.find_elements(By.CLASS_NAME, 'most-popular__post')

        for section in most_popular_list:
            try:
                # Extract title, category, and URL from most popular section
                title = section.find_element(By.CLASS_NAME, 'post__title').text
                category = section.find_element(By.CSS_SELECTOR, 'h4.post__category').text
                url = section.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")

                # Visit each article URL
                retry_load(driver, url)

                # Extract body text, publication date, and source domain
                body_text = " ".join([p.text for p in driver.find_elements(By.TAG_NAME, "p")])
                try:
                    publication_date = driver.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
                except:
                    publication_date = "Not Available"
                
                source_domain = urlparse(driver.current_url).netloc

                # Store the article data from the most popular section
                articles_data.append({
                    "Title": title,
                    "Category": category,
                    "Body Text": body_text,
                    "Publication Date": publication_date,
                    "Source Domain": source_domain,
                    "URL": url
                })

                # Return to the main page
                driver.back()
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"Error processing most popular article: {e}")
    except Exception as e:
        print(f"Error finding secondary mobile section: {e}")

except Exception as e:
    print(f"Error loading page: {e}")

# Save data as JSON
with open('scraped_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=4)

# Insert data into MongoDB
insert_data('scraped_articles.json')

driver.quit()
