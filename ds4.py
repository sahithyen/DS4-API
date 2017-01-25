import time
import hid


class DS4(object):

    def __init__(self, deviceInfo):
        self.device = hid.device()

        self.device.open_path(deviceInfo['path'])

        self.__rumbleRight = 0
        self.__rumbleLeft = 0
        self.__red = 0
        self.__green = 0
        self.__blue = 0
        self.__onDuration = 0
        self.__offDuration = 0
        pass

    def setRumble(self, right, left):
        self.__rumbleRight = right
        self.__rumbleLeft = left

        self.__updateActuator()
        pass

    def setLightbarColor(self, red, green, blue, on=0, off=0):
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__onDuration = on
        self.__offDuration = off

        self.__updateActuator()
        pass

    def update(self):
        data = self.device.read(64)
        offset = 0

        dPad = data[5 + offset] & 0x0F
        self.up = dPad == 0 or dPad == 1 or dPad == 7
        self.right = dPad == 1 or dPad == 2 or dPad == 3
        self.down = dPad == 3 or dPad == 4 or dPad == 5
        self.left = dPad == 5 or dPad == 6 or dPad == 7
        self.square = (data[5 + offset] & 0x10) != 0
        self.cross = (data[5 + offset] & 0x20) != 0
        self.circle = (data[5 + offset] & 0x40) != 0
        self.triangle = (data[5 + offset] & 0x80) != 0
        self.l1 = (data[6 + offset] & 0x01) != 0
        self.r1 = (data[6 + offset] & 0x02) != 0
        self.l2 = (data[6 + offset] & 0x04) != 0
        self.r2 = (data[6 + offset] & 0x08) != 0
        self.share = (data[6 + offset] & 0x10) != 0
        self.options = (data[6 + offset] & 0x20) != 0
        self.l3 = (data[6 + offset] & 0x40) != 0
        self.r3 = (data[6 + offset] & 0x80) != 0
        self.trackPadButton = (data[7 + offset] & 2) != 0
        self.psButton = (data[7 + offset] & 1) != 0

        self.leftAnalogX = data[1 + offset]
        self.leftAnalogY = data[2 + offset]
        self.rightAnalogX = data[3 + offset]
        self.rightAnalogY = data[4 + offset]
        self.l2Analog = data[8 + offset]
        self.r2Analog = data[9 + offset]

        self.timestamp = data[7 + offset] >> 2
        pass

    def __updateActuator(self):
        self.device.write([
            0x05,
            0xff,
            0x04,
            0x00,
            self.__rumbleRight,
            self.__rumbleLeft,
            self.__red,
            self.__green,
            self.__blue,
            self.__onDuration,
            self.__offDuration
        ])
        pass

    def __del__(self):
        self.device.close()
        pass
