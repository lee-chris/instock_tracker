import urllib.request

#url = "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-zelda/5723538.p?skuId=5723538"
url = "http://www.bestbuy.com/site/nintendo-amiibo-figure-alm-celica-2-pack/5746603.p?skuId=5746603"

# get html for product page
data = urllib.request.urlopen(url).read()

# look for text indicating that the item is sold out
sold_out = str(data).find("SOLD_OUT_ONLINE") > -1

print(sold_out)
