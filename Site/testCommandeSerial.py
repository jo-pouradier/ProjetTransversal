import serial

ser = serial.Serial('/dev/ttyUSB0')#change this to the name of your port
ser.baudrate = 115200 
ser.write("avancerR\n\r".encode())
ser.close()
print("avancerR")