import requests #pip install requests
#import urllib.request
import credentials
import multiprocessing

def send(turbine_id, endtime, starttime, birdminutes, speed,
         temperature, humidity):
    url = "http://folk.ntnu.no/sigurdht/fugl.xyz/api/register/"
    # url = "http://www.asfwwwrrr.no/"
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

def call_with_timeout(func, args, timeout):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # define a wrapper of `return_dict` to store the result.
    def function(return_dict):
        return_dict['value'] = func(*args)

    p = multiprocessing.Process(target=function, args=(return_dict,))
    p.start()

    # Force a max. `timeout` or wait for the process to finish
    p.join(timeout)

    # If thread is still active, it didn't finish: raise TimeoutError
    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError
    else:
        return return_dict['value']

if __name__ == "__main__":
    # for testing purposes
    import datetime
    import threading
    
    end = datetime.datetime.now()
    start = end - datetime.timedelta(0,10,0)
    try:
        call_with_timeout(send, (2, end, start, 0.1, 4.0, 15.3, 34.3), 2)
    except:
        print("jj")
    # sendthread = threading.Thread(target = send, args = (2, end, start, 0.1, 4.0, 15.3, 34.3))
    # sendthread.start()
    # sendthread.join(timeout = 3)
    print("hallo?")
