import requests
session = requests.Session()
session.trust_env = False
response = session.get("http://192.168.43.214:5000/video_feed")

print response  
