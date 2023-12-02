#!/usr/bin/python 
# -*- coding: utf-8 -*-
"""
Считываем данные с портативного дозиметра AtomFast (Bluetooth Low Energy)
"""

from bluepy import btle
import struct

MAC_ADDR = 'A8:10:87:22:40:40'


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global arr

        curr_intensity = struct.unpack('<f', data[5:9])[0]  # интенсивность излучения в мкЗв/ч

        try:
            arr
        except NameError:
            arr = []
        arr.append(curr_intensity)
        if len(arr) > 5:
            del arr[0]
        avg_intencity = sum(arr) / len(arr)
        print(u'Intencity AVG:{:4.2} \u03BCSv/h CURRENT:{:4.2} \u03BCSv/h'.format(avg_intencity, curr_intensity))
        print(u'Dose: {:6.4} mSv'.format(struct.unpack('<f', data[1:5])[0]))
        print(u'CPS last 2 seconds: {}'.format(struct.unpack('<H', data[9:11])[0]))
        print(u'Temperature: {}\u2103'.format(data[12]))
        print(u'Battery: {}%'.format(data[11]))
        print('---')


# start  -------
print("Connecting...")
atomble = btle.Peripheral(MAC_ADDR)
atomble.setDelegate(MyDelegate())

try:
    # активируем отправку уведомлений
    atomble.writeCharacteristic(0x27, struct.pack('<bb', 0x01, 0x00))
    while True:
        if atomble.waitForNotifications(1.0):
            continue
finally:
    atomble.disconnect()
    print("Disconnected")
