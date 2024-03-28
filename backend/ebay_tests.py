import unittest
from unittest.mock import patch, MagicMock
from ebay import Trader
import database
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore_async

class EbayApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_database(self):
        found = False
        doc_ref = database.db.collection("usernames").document("testuser7")
        await doc_ref.set({"email": "testuser7@example.com", "userId": "Ks3LFPD32pey4mAg1R11YDZKwIA2", "username": "testuser7"})

        users_ref = database.db.collection("usernames")
        docs = users_ref.stream()
        async for doc in docs:
            if doc.to_dict() == {'userId': 'Ks3LFPD32pey4mAg1R11YDZKwIA2', 'email': 'testuser7@example.com', 'username': 'testuser7'}:
                found = True
                break
        
        self.assertEqual(found, True)
    
    async def test_check_api(self):
        ebay_api = Trader()
        connected = False
        if ebay_api.api.session != None:
            connected = True
        self.assertEqual(connected, True)
    
    async def test_messages(self):
        ebay_api = Trader()
        response = ebay_api.get_messages()

        self.assertGreaterEqual(response, 0)

if __name__ == '__main__':
    unittest.main()

