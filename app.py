from flask import Flask, request
import pymongo
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://sanket:<db_password>@cluster0.rnfqhf5.mongodb.net/")
db = client["github_events"]
collection = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    author = data['sender']['login']
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    event = {
        "author": author,
        "event_type": event_type,
        "timestamp": timestamp
    }

    # Store the event
    collection.insert_one(event)
    return 'webhook received', 200

if __name__ == '__main__':
    app.run(port=5000)
