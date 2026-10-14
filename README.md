# Raspberry Pi S3 Scraper & Kiosk Setup 🍓☁️

Turnkey web scraping and automated data pipeline running on Raspberry Pi, uploading structured JSON datasets directly to an Amazon AWS S3 bucket on a schedule.

Includes an onboard touchscreen GUI configuration panel for headless or standalone setup.

---

## 🚀 Features

- **Automated Web Scraping:** Headless extraction using `requests` and `BeautifulSoup4`.
- **AWS S3 Integration:** Direct, timed payload uploads via `boto3`.
- **Onboard Touchscreen Setup:** Tkinter-based configuration GUI to enter credentials without modifying code.
- **Background Daemon:** Runs automatically as a `systemd` service on boot.
- **Zero Secrets Leak:** Built with `.env` separation for safe open-source distribution.

---

## 🛠️ Hardware Requirements

- Raspberry Pi 3 Model B/B+ (or newer)
- Raspberry Pi Display (or any HDMI/DSI touchscreen/monitor)
- MicroSD Card (16GB+)
- 5V Power Supply

---

## 📦 Project Structure

```text
rpi-s3-scraper/
├── .env.example          # Configuration template
├── .gitignore            # Ignores secrets, logs, venv
├── requirements.txt      # Python dependencies
├── setup_ui.py           # GUI setup interface
├── scraper_service.py    # Scraping & S3 background daemon
└── README.md             # Documentation
