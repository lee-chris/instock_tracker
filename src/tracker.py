import urllib.request

def get_urls():
    """Get the urls to track"""
    
    urls = []
    
    urls.append("http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-zelda/5723538.p?skuId=5723538")
    urls.append("http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-guardian/5723700.p?skuId=5723700")
    urls.append("http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-link-archer/5723537.p?skuId=5723537")
    urls.append("http://www.bestbuy.com/site/nintendo-amiibo-figure-alm-celica-2-pack/5746603.p?skuId=5746603")
    
    return urls


def print_status(urls):
    """Print the status of each url
    
    Args:
        urls: array of urls to check
    """
    
    for url in urls:
        
        # get html for product page
        data = urllib.request.urlopen(url).read()
        
        # look for text indicating that the item is sold out
        sold_out = str(data).find("SOLD_OUT_ONLINE") > -1
        
        print(url)
        print("Sold out: " + str(sold_out))


# print the status of each url
print_status(get_urls())
