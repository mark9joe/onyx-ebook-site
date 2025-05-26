import json
import random

def get_random_post():
    with open("content_pool.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return random.choice(data)

# Example usage
if __name__ == "__main__":
    post = get_random_post()
    print(f"Title: {post['title']}")
    print(f"URL: {post['url']}")
    print(f"Description: {post['description']}")
