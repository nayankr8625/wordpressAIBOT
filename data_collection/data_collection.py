from bs4 import BeautifulSoup
import requests
import time

# Set the base URL for your WordPress site
WORDPRESS_DOMAIN = "portfo336.wordpress.com"
BASE_URL = f"https://public-api.wordpress.com/rest/v1.1/sites/{WORDPRESS_DOMAIN}/posts"

# Function to fetch the latest posts
def fetch_latest_posts(url, limit=5):
    response = requests.get(url , params={"per_page": limit})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch posts: {response.status_code}")
    
def clean_content(content:str):
    # Parsing the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Extracting the plain text without HTML tags
    plain_text = soup.get_text()

    # Printing the cleaned text
    return plain_text

def extract_content_as_json():
    all_posts = fetch_latest_posts(url=BASE_URL)
    posts_json = []  # List of dictionaries to store post information
    
    for post in all_posts["posts"]:
        # Create a dictionary for each post
        post_dict = {
            "title": post["title"],
            "content": clean_content(post["content"]),
            "short_url": post["short_URL"],
        }
        # Add the dictionary to the list of posts
        posts_json.append(post_dict)

    return posts_json