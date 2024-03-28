import firebase_admin
from firebase_admin import credentials, firestore_async

cred = credentials.Certificate("creds.json")
app = firebase_admin.initialize_app(cred)
db = firestore_async.client()

async def add_listing_to_db(title, description, seller, item, listing_id, price, condition, listing_date):
    doc_ref = db.collection("listings").document(title)
    await doc_ref.set({"listing information": {"seller": seller, "item": item, "listing id": listing_id, "price": price, "condition": condition, "date listed": listing_date, "description": description}})
    return True
