import urllib.request
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
burl = "https://builder.blender.org"
response = urllib.request.urlopen(burl, context= ssl_context)
data = response.read()
body = data.decode("utf-8")
print("body", body)