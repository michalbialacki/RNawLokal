import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import asyncio
import concurrent.futures

"""
Wysyłanie danych do Real-time DataBase od Firebase
W przypadku wykonywania tej metody sekwencyjnie dla zestawu testowego
czas wykonywania aplikacji wynosił 77sek

Wykonywanie bez tej metody zajęło 22sek
"""

cred = credentials.Certificate('system_pozycjonowania.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://czystysystempozycjonowania-default-rtdb.firebaseio.com/'
})

def update_firebase(wspolrzedna_x_uzytkownika, wspolrzedna_y_uzytkownika, anchorID = "Warsaw"):

    ref = db.reference('/Zachowane Wspolrzedne')
    ref.child(anchorID).update({
        'wspolrzednaXSB3': str(wspolrzedna_x_uzytkownika),
        'wspolrzednaYSB3': str(wspolrzedna_y_uzytkownika)
    })


