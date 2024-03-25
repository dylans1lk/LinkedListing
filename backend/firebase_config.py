import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate('D:\linkedlisting-firebase-adminsdk-3kmtu-9b1620ef63.json')
firebase_admin.initialize_app(cred)
