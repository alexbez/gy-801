from machine import Pin,I2C
import math
import time

SCL_PIN = const(22)
SDA_PIN = const(21)
I2C_ADDR = const(0x53)

regAddress = const(0x32)
TO_READ = 6
buff = bytearray(6)

class ADXL345:
    def __init__(self,scl=SCL_PIN, sda=SDA_PIN,addr=I2C_ADDR):
        self.addr = addr
        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        b = bytearray(1)
        b[0] = 0
        self.i2c.writeto_mem(self.addr,0x2d,b)
        b[0] = 16
        self.i2c.writeto_mem(self.addr,0x2d,b)
        b[0] = 8
        self.i2c.writeto_mem(self.addr,0x2d,b)

    @property
    def xValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        x = (int(buff[1]) << 8) | buff[0]
        if x > 32767:
            x -= 65536
        return x
   
    @property
    def yValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        y = (int(buff[3]) << 8) | buff[2]
        if y > 32767:
            y -= 65536
        return y
     
    @property   
    def zValue(self): 
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        z = (int(buff[5]) << 8) | buff[4]
        if z > 32767:
            z -= 65536
        return z
           
    def RP_calculate(self,x,y,z):
        roll = math.atan2(y , z) * 57.3
        pitch = math.atan2((- x) , math.sqrt(y * y + z * z)) * 57.3
        return roll,pitch
