# import code for encoding urls and generating md5 hashes
import urllib, hashlib
 
# Set your variables here
email = "ky3466214728@gmail.com"
default = "https://ikebo.cn/static/default_avatar.jpg"
size = 40
 
# construct the url
gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

print(gravatar_url)