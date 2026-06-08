import json
from http.server import BaseHTTPRequestHandler

from pymongo import MongoClient

# Your MongoDB Connection String
MongoURI = "mongodb+srv://maiSakura:daneshmuthu@iotadmin.qhxngyt.mongodb.net/?retryWrites=true&w=majority&appName=iotadmin"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Connect to MongoDB
            client = MongoClient(MongoURI, serverSelectionTimeoutMS=5000)
            db_collection = client.PowerPlantDB.StatusCollection

            # Fetch the status document
            status_doc = db_collection.find_one()
            alarm_status = "False"

            if status_doc:
                alarm_status = status_doc.get("alarm", "False")

            # Send the successful JSON response to your HTML frontend
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")

            # --- CRITICAL FIX: Tell Vercel NEVER to cache this API response ---
            self.send_header(
                "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
            )

            self.end_headers()
            self.wfile.write(json.dumps({"alarm": alarm_status}).encode("utf-8"))

        except Exception as e:
            # If database fails, return an error state safely
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header(
                "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
            )
            self.end_headers()
            self.wfile.write(
                json.dumps({"alarm": "False", "error": str(e)}).encode("utf-8")
            )
