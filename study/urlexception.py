from urllib import request
from urllib import error

try:
    request.urlopen("http://blog.baidusss.net")
except error.HTTPError as e:
    print(e.code)
    print(e.reason)
except error.URLError as e:
    print(e.reason)

# 或者合并到一起
try:
    request.urlopen("http://blog.baidusss.net")
except error.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)