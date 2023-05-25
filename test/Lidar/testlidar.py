from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)
liste =[[]*10]
flag=0
for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' %(i, len(scan)))
    print(scan)
    for i in range(len(scan)):
        if (scan[i][1]>=330 or scan[i][1]<=30):
            if scan[i][2]<=1000:
                flag=1
    print(flag)
    break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()