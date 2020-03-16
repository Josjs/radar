def get():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as fil:
        temp = int(fil.read())
        return temp/1000.0

