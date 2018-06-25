import smbus
bus=smbus.SMBus(1)
import time

LSM9DS0=1

def detectIMU():
    global LSM9DS0

    try:
        LSM9DS0_WHO_G_response=(bus.read_byte_data(0x6A, 0x0F))
        LSM9DS0_WHO_XM_response=(bus.read_byte_data(0x1E, 0x0F))
    except IOError as e:
        print' '
    else:
       if(LSM9DS0_WHO_G_response==0xd4) and (LSM9DS0_WHO_XM_response==0x49):
            print"Found LSM9DS0"
            LSM9DS0=1

    try:
        LSM9DS1_WHO_XG_response=(bus.read_byte_data(0x6A, 0x0F))
        LSM9DS1_WHO_M_response=(bus.read_byte_data(0x1C, 0x0F))
    except IOError as f:
       print' '
    else:
      if(LSM9DS1_WHO_XG_response==0x68) and (LSM9DS1_WHO_M_response==0x3d):
          print"Found LSM9DS1"
          LSM9DS0=0

time.sleep(1)

def writeACC(register, value):
    if(LSM9DS0):
        bus.write_byte_data(0x1E,register,value)
    else:
        bus.write_byte_data(0x6A,register,value)
    return -1    


def readACCx():
    if(LSM9DS0):
      acc_l=bus.read_byte_data(0x1E, 0x28)
      acc_h=bus.read_byte_data(0x1E, 0x29)
    else:
      acc_l=bus.read_byte_data(0x6A, 0x28)
      acc_h=bus.read_byte_data(0x6A, 0x29)

    acc_combined=(acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536

def readACCy():
    if(LSM9DS0):
      acc_l=bus.read_byte_data(0x1E, 0x2A)
      acc_h=bus.read_byte_data(0x1E, 0x2B)
    else:
      acc_l=bus.read_byte_data(0x6A, 0x2A)
      acc_h=bus.read_byte_data(0x6A, 0x2B)

    acc_combined=(acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536

def readACCz():
    if(LSM9DS0):
      acc_l=bus.read_byte_data(0x1E, 0x2C)
      acc_h=bus.read_byte_data(0x1E, 0x2D)
    else:
      acc_l=bus.read_byte_data(0x6A, 0x2C)
      acc_h=bus.read_byte_data(0x6A, 0x2D)

    acc_combined=(acc_l | acc_h << 8)

    return acc_combined if acc_combined < 32768 else acc_combined - 65536

def initIMU():
    if(LSM9DS0):
        writeACC(0x20, 0b01100111)
        writeACC(0x21, 0b00011000)

    else:
        writeACC(0x1F, 0b00111000)
        writeACC(0x20, 0b00111000)
            
