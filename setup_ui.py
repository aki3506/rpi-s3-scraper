import os
import tkinter as tk
from tkinter import messagebox

ENV_FILE = os.path.expanduser("~/rpi-s3-scraper/.env")
ENV_EXAMPLE = os.path.expanduser("~/rpi-s3-scraper/.env.example")

def load_current_env():
    data = {}
    target = ENV_FILE if os.path.exists(ENV_FILE) else ENV_EXAMPLE
    if os.path.exists(target):
        with open(target, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    data[k] = v
    return data

def save_env(entries, root):
    with open(ENV_FILE, "w") as f:
        for key, entry in entries.items():
            f.write(f"{key}={entry.get().strip()}\n")
    messagebox.showinfo("Başarılı", "Ayarlar kaydedildi! Servis başlatılıyor...")
    root.destroy()
    os.system("sudo systemctl restart s3-scraper.service")

def main():
    current_data = load_current_env()

    root = tk.Tk()
    root.title("Pi S3 Scraper Setup")
    root.geometry("800x480")
    root.attributes("-fullscreen", True)

    tk.Label(root, text="Sistem Yapılandırma Paneli", font=("Arial", 16, "bold")).pack(pady=10)

    entries = {}
    fields = [
        ("AWS_ACCESS_KEY_ID", "AWS Access Key:"),
        ("AWS_SECRET_ACCESS_KEY", "AWS Secret Key:"),
        ("AWS_REGION", "AWS Region:"),
        ("S3_BUCKET_NAME", "S3 Bucket Adı:"),
        ("TARGET_URL", "Hedef URL:"),
        ("SCRAPE_INTERVAL_MINUTES", "Çalışma Aralığı (Dakika):")
    ]

    form_frame = tk.Frame(root)
    form_frame.pack(fill="both", expand=True, padx=20)

    for idx, (key, label_text) in enumerate(fields):
        tk.Label(form_frame, text=label_text, font=("Arial", 10), anchor="w").grid(row=idx, column=0, sticky="w", pady=4)
        entry = tk.Entry(form_frame, font=("Arial", 11), width=45)
        entry.insert(0, current_data.get(key, ""))
        entry.grid(row=idx, column=1, pady=4, padx=10)
        entries[key] = entry

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Kaydet ve Başlat", font=("Arial", 12, "bold"), bg="#28a745", fg="white",
              padx=15, pady=5, command=lambda: save_env(entries, root)).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Kapat / Masaüstü", font=("Arial", 10),
              command=root.destroy).pack(side="left")

    root.mainloop()

if __name__ == "__main__":
    main()
