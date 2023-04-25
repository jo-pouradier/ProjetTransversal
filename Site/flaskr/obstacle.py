from rplidar import RPLidar


def obstacle():
    lidar = RPLidar('/dev/ttyUSB0')
    flag=0
    for i, scan in enumerate(lidar.iter_scans()):
        # print('%d: Got %d measurments' %(i, len(scan)))
        # print(scan)
        # print(lidar.iter_scans())
    # scan=lidar.iter_scans()[0]
        # print("test scan : " , scan)
        for i in range(len(scan)):
            if (scan[i][1]>=330 or scan[i][1]<=30):
                if scan[i][2]<=1000:
                    flag=1

        print(flag)  
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()  
        return(flag==1)

