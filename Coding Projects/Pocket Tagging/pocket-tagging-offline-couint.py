from bs4 import BeautifulSoup

with open("pocket_export.html", "r") as f:
    soup = BeautifulSoup(f, "html.parser")
articles = soup.find_all("li")
tagged_count = sum(1 for li in articles if li.get("tags"))
print(f"Total articles in export: {len(articles)}")
print(f"Tagged articles from export: {tagged_count}")
