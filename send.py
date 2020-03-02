import requests #pip install requests
import credentials

def send(turbine_id, endtime, starttime, birdminutes, topspeed,
         temperature, humidity):
    url = "http://folk.ntnu.no/sigurdht/fugl.xyz/api/register/"
    data = {
    	"db_username":          credentials.username,
    	"db_password":          credentials.password,
    	"turbine_id":           turbine_id,
        "endtime":              endtime,
        "starttime":            starttime,
        "birdminutes":          birdminutes,
    	"topspeed":             topspeed,
        "temperature":          temperature,
        "humidity":             humidity
    }
    r = requests.post(url, data, allow_redirects=False)

