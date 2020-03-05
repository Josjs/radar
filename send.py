import requests #pip install requests
import credentials

def send(turbine_id, endtime, starttime, birdminutes, speed,
         temperature, humidity):
    url = "http://folk.ntnu.no/sigurdht/fugl.xyz/api/register/"
    data = {
    	"db_username":          credentials.username,
    	"db_password":          credentials.password,
    	"turbine_id":           turbine_id,
        "endtime":              endtime.isoformat(),
        "starttime":            starttime.isoformat(),
        "birdminutes":          birdminutes,
    	"speed":                speed,
        "temperature":          temperature,
        "humidity":             humidity
    }
    r = requests.post(url, data, allow_redirects=False)

