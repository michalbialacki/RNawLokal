import pyrebase

def getXY():
    firebaseconfig={
        'apiKey': "AIzaSyAdZMqPX_4MYdrXrQes9feFmsytDVDBJsY",
        'authDomain': "czystysystempozycjonowania.firebaseapp.com",
        'databaseURL': "https://czystysystempozycjonowania-default-rtdb.firebaseio.com",
        'projectId' :"czystysystempozycjonowania",
        'storageBucket': "czystysystempozycjonowania.appspot.com",
        'messagingSenderId': "361380612353",
        'appId': "1:361380612353:web:1110ce4cac680bc2df7300",
        'measurementId': "G-MG7BM1XTSH"
    }

    firebase=pyrebase.initialize_app(firebaseconfig)
    systemPozycjonowania=firebase.database()

    data ={
        'Test0':'Witam',
        'Test1':'Szanowni',
        'Test3':'Panstwo',
    }

    userCoordinates= systemPozycjonowania.child("Zachowane Współrzędne").child("Wskazane Współrzędne Użytkownika").get().val()
    return userCoordinates['wspolrzednaXSB3'],userCoordinates['wspolrzednaYSB3']