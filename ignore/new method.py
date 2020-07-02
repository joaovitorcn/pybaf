
import pandas as pd
import urllib.request, json
from unidecode import unidecode


uf = "RS"
cep = '90040192'
city = 'Porto Alegre'
add = 'Av Venancio Aires'
num = "462"
key = 'An0tJWGs83w7ztI_6YlTDd64Sn-2SECjgeEOLRnw-CzENRqmTHiyno0pwdPpbwCw'

inputs = [uf,cep,city,add,num,key]


inputs = [x.replace(" ", "%20") for x in inputs]

s = 'http://dev.virtualearth.net/REST/v1/Locations/BR/{0}/{1}/{2}/{3}%20{4}?&key={5}'

url = s.format(*inputs)


translationTable = str.maketrans("éàèùâêîôûçãáõóÉÀÈÙÂÊÎÔÛÇÃÁÕÓ", "eaeuaeioucaaooEAEUAEIOUCAAOO")
url = url.translate(translationTable)
url = unidecode(url)
print(url)

try:
    response = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    raise KeyError("error")

# or do your custom error message handling here

data = json.loads(response.read())

print(data['resourceSets'][0]['resources'][0]['point']['coordinates'])



