import requests
from bs4 import BeautifulSoup
import os
import json

folders = [
    "data/aws",
    "data/gcp",
    "data/finops",
    "data/kaggle"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

sources = {
    "aws": {
        "pricing": "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html",
        "billing": "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/",
        "blogs": "https://aws.amazon.com/blogs/aws-cost-management/"
    },
    "gcp": {
        "pricing": "https://cloud.google.com/pricing",
        "billings": "https://cloud.google.com/billing/docs/how-to",
        "blogs": "https://cloud.google.com/blog/topics/cost-management"
    },
    "finops": {
        "framework": "https://www.finops.org/introduction/what-is-finops/"
    },
    "kaggle":{
        "datasets": "https://www.kaggle.com/datasets?search=cloud+cost"
    }
}

urls = [
    "https://aws.amazon.com/blogs/aws-cost-management/",
    "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/",
    "https://aws.amazon.com/ec2/pricing/",
    "https://cloud.google.com/pricing",
    "https://cloud.google.com/billing/docs/how-to",
    "https://cloud.google.com/blog/topics/cost-management",
    "https://www.finops.org/introduction/what-is-finops/",
    "https://www.kaggle.com/datasets?search=cloud+cost"
]

def clean_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    return "\n".join(lines)


for url in urls:
    print(f"Processing: {url}")
    cleaned = clean_url(url)

documents = [] 

for category, docs in sources.items():
    for name, url in docs.items():
        print(f"Processing {category} - {name}")
        
        cleaned_text = clean_url(url)

        file_path = f"data/{category}/{name}.txt"
        
        with open(file_path, "w") as f:
            f.write(cleaned_text)
        documents.append({
            "source": url,
            "category": category,
            "content": cleaned_text
        })

with open("data/metadata.json", "w") as f:
    json.dump(documents, f, indent=2)