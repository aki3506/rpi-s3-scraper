import os
import time
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import boto3
from dotenv import load_dotenv

ENV_PATH = os.path.expanduser("~/rpi-s3-scraper/.env")

def run_pipeline():
    load_dotenv(ENV_PATH, override=True)
    target_url = os.getenv("TARGET_URL")
    bucket_name = os.getenv("S3_BUCKET_NAME")
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "eu-central-1")

    if not all([target_url, bucket_name, aws_key, aws_secret]):
        print(f"[{datetime.now()}] Yapilandirma eksik, bekleniyor...")
        return False

    headers = {"User-Agent": "Mozilla/5.0 (Compatible; PiScraperBot/1.0)"}
    resp = requests.get(target_url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    titles = [t.get_text(strip=True) for t in soup.find_all(["h1", "h2"])]

    payload = {
        "source": target_url,
        "scraped_at": datetime.utcnow().isoformat(),
        "item_count": len(titles),
        "data": titles
    }

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region
    )

    now = datetime.utcnow()
    s3_key = f"scrapes/{now.strftime('%Y-%m-%d')}/data_{now.strftime('%H%M%S')}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"),
        ContentType="application/json"
    )
    print(f"[{datetime.now()}] Basariyla S3'e yuklendi: {s3_key}")
    return True

def main():
    while True:
        try:
            if not os.path.exists(ENV_PATH):
                print(f"[{datetime.now()}] .env dosyasi bulunamadi, bekleniyor...")
                time.sleep(15)
                continue

            success = run_pipeline()
            interval_min = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "60"))
            time.sleep(interval_min * 60 if success else 30)

        except Exception as e:
            print(f"[{datetime.now()}] Hata: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
