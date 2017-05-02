import configparser
import item
import smtplib
import urllib.request

def get_items():
    """Get the items to track"""
    
    items = []
    
    items.append(item.Item(
        "Breath of the Wild Zelda Amiibo",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-zelda/5723538.p?skuId=5723538"))
    
    items.append(item.Item(
        "Breath of the Wild Guardian Amiibo",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-guardian/5723700.p?skuId=5723700"))
    
    items.append(item.Item(
        "Breath of the Wild Link Archer Amiibo",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-link-archer/5723537.p?skuId=5723537"))
    
    return items


def get_status(items):
    """Get the status of each item"""
    
    for item in items:
        
        # get html for product page
        data = urllib.request.urlopen(item.url).read()
        
        # look for text indicating that the item is sold out
        sold_out = str(data).find("SOLD_OUT_ONLINE") > -1
        
        item.set_status(sold_out)
        
        # print out status
        print(item.name + " - sold out: " + str(item.sold_out))


def send_email(subject, msg):
    """Send an email message using the settings in tracker.ini"""
    
    config = configparser.ConfigParser()
    config.read("tracker.ini")
    
    server = smtplib.SMTP(config["smtp"]["server"])
    server.ehlo()
    server.starttls()
    server.login(config["smtp"]["username"], config["smtp"]["password"])
    
    body = "\r\n".join([
        "From: " + config["message"]["from"],
        "To: " + config["message"]["to"],
        "Subject: " + subject,
        "",
        msg
        ])
    
    server.sendmail(config["message"]["from"], config["message"]["to"], body)
    server.close()


def main():
    
    # print the status of each url
    items = get_items()
    get_status(items)
    
    send_email("InStock Tracker - Test Message", "test")


if __name__ == "__main__":
    main()
