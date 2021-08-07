from djitellopy import tello
import numpy as np
import FirebaseGetCoordinates

def movementAlgorythm(dronePosition=[0.00,0.00],userPosition=(0.00,0.00)):
    Xmovement=int((((dronePosition[0]**2)+(userPosition[0]**2))**0.5)*100)
    Ymovement=int((((dronePosition[1]**2)+(userPosition[1]**2))**0.5)*100)
    me=tello.Tello()
    me.connect()
    print(me.get_battery())
    me.takeoff()

    while not((abs(userPosition[0])-0.1<=abs(dronePosition[0])<=abs(userPosition[0])+0.1) and (abs(userPosition[1])-0.1<=abs(dronePosition[1])<=abs(userPosition[1])+0.1)):
        if dronePosition[0]>userPosition[0]:
            me.move_left(Xmovement)
            correctPositionX(dronePosition,userPosition,Xmovement)
        elif dronePosition[0]<userPosition[0]:
            me.move_right(Xmovement)
            correctPositionX(dronePosition,userPosition,Xmovement)
        else:
            pass
        if dronePosition[1]>userPosition[1]:
            me.move_back(Ymovement)
            correctPositionY(dronePosition,userPosition,Ymovement)
        elif dronePosition[1]<userPosition[1]:
            me.move_forward(Ymovement)
            correctPositionY(dronePosition,userPosition,Ymovement)
        else:
            pass
        #X movement coordinates
#shoot
            #Y movement coordinates


    print(dronePosition)
    if((0.9*userPosition[0]<=dronePosition[0]<=1.1*userPosition[0]) and (0.9*userPosition[1]<=dronePosition[1]<=1.1*userPosition[1])):
        print("True")


    me.land()

def correctPositionX(dronePosition,userPosition,Xmovement):
    if dronePosition[0] <= 0.00 and userPosition[0] >= 0.00:
        dronePosition[0] += (Xmovement / 100)
    else:
        dronePosition[0] -= (Xmovement / 100)

def correctPositionY(dronePosition,userPosition,Ymovement):
    if dronePosition[1] <= 0.00 and userPosition[1] >= 0.00:
        dronePosition[1] += (Ymovement / 100)
    else:
        dronePosition[1] -= (Ymovement / 100)



wspolrzednaX,wspolrzednaY=FirebaseGetCoordinates.getXY()
movementAlgorythm([0.00,0.00],(wspolrzednaX,wspolrzednaY))

