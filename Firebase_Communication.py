import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('system_pozycjonowania.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://czystysystempozycjonowania-default-rtdb.firebaseio.com/'
})

def update_firebase(wspolrzedna_x_uzytkownika, wspolrzedna_y_uzytkownika):

    ref = db.reference('/Zachowane Współrzędne')
    ref.child('Wskazane Współrzędne Użytkownika').update({
        'wspolrzednaXSB3': wspolrzedna_x_uzytkownika,
        'wspolrzednaYSB3': wspolrzedna_y_uzytkownika
    })
