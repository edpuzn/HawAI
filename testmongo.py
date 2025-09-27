from pymongo import MongoClient
from pymongo.errors import PyMongoError
import sys, time

# Paroladaki ? işaretini encode ediyoruz
URI = "mongodb://rwuser:Mu2190541%3F@124.243.175.197:8635,188.239.49.153:8635/test?authSource=admin"

def log(msg):
    print(msg, flush=True)

try:
    log("[1/4] Bağlantı kuruluyor...")
    client = MongoClient(URI, serverSelectionTimeoutMS=15000, socketTimeoutMS=15000, connectTimeoutMS=15000)
    log("[2/4] Ping gönderiliyor...")
    log(client.admin.command("ping"))
    log("[3/4] Yaz/oku testi...")
    db = client["hawai_test"]
    col = db["healthcheck"]
    doc_id = col.insert_one({"ok": True, "t": int(time.time())}).inserted_id
    found = col.find_one({"_id": doc_id})
    log(found)
    col.delete_one({"_id": doc_id})
    log("[4/4] OK")
except PyMongoError as e:
    log(f"Mongo hata: {e}")
    sys.exit(1)