import amazon
import configparser
import datetime
import smtplib
import time
import urllib.request

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from item import Item
from item import Status

def get_items():
    """Get the items to track."""
    
    items = []
    
    items.append(Item(
        "Breath of the Wild Zelda Amiibo - Bestbuy.com",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-zelda/5723538.p"))
    
    items.append(Item(
        "Breath of the Wild Guardian Amiibo - Bestbuy.com",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-guardian/5723700.p"))
    
    items.append(Item(
        "Breath of the Wild Link Archer Amiibo - Bestbuy.com",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-the-legend-of-zelda-breath-of-the-wild-series-link-archer/5723537.p"))
    
    items.append(Item(
        "Breath of the Wild Zelda Amiibo - Amazon.com",
        "https://www.amazon.com/Nintendo-amiibo-Zelda-Breath-Wild-wii-u/dp/B01N10NIBP",
        "Breath of the Wild Zelda Amiibo"))
    
    items.append(Item(
        "Breath of the Wild Guardian Amiibo - Amazon.com",
        "https://www.amazon.com/Nintendo-amiibo-Guardian-Breath-Wild-wii-u/dp/B01N6QPWBV",
        "Breath of the Wild Guardian Amiibo"))
    
    items.append(Item(
        "Breath of the Wild Link Archer Amiibo - Amazon.com",
        "https://www.amazon.com/Nintendo-amiibo-Link-Archer-Breath-wii-u/dp/B01N4NTNO2",
        "Breath of the Wild Link Archer Amiibo"))
    
    items.append(Item(
        "Breath of the Wild Link Rider Amiibo - Amazon.com",
        "https://www.amazon.com/Nintendo-amiibo-Link-Rider-Breath-wii-u/dp/B01N33LIXR"))
    
    items.append(Item(
        "Breath of the Wild Bokoblin Amiibo - Amazon.com",
        "https://www.amazon.com/Nintendo-amiibo-Bokoblin-Breath-Wild-wii-u/dp/B01N33OBYK"))
    
    """
    items.append(Item(
        "Super Smash Bros Cloud Amiibo",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-super-smash-bros-cloud/5433400.p"))
    
    items.append(Item(
        "Super Smash Bros Mega Man Amiibo",
        "http://www.bestbuy.com/site/nintendo-amiibo-figure-super-smash-bros-series-mega-man/1378006.p"))
    """
    
    return items


def get_status_bestbuy(html):
    """Parse the product status from bestbuy.com html."""
    
    html = str(html)
    
    # find the cart button div
    start = html.find("<div class=\"cart-button\"")
    end = html.find(">", start + 1)
    
    button_div = html[start:end + 1]
    
    # find the data-button-state-id attribute
    state_start = button_div.find("data-button-state-id=\"")
    state_end = button_div.find("\"", state_start + 22)
    
    status = button_div[state_start + 22:state_end]
    
    if status == "SOLD_OUT_ONLINE":
        return Status.SOLD_OUT
    elif status == "PRE_ORDER":
        return Status.PRE_ORDER
    elif status == "ADD_TO_CART":
        return Status.IN_STOCK
    else:
        return Status.UNKNOWN


def get_status_amazon(html):
    """Parse the product status from amazon.com html."""
    
    html = str(html)
    
    # simply look for an add to cart button
    # TODO add parsing to identify preorders
    if html.find("input id=\"add-to-cart-button") == -1:
        return Status.SOLD_OUT
    
    # if there is a "Fulfilled by Amazon" link
    # I only care about the sold by amazon.com items
    elif html.find("SSOFpopoverLink") != -1:
        return Status.SOLD_OUT
    
    else:
        return Status.IN_STOCK


def get_status(items):
    """Get the status of each item."""
    
    instock_items = []
    
    for item in items:
        
        #if item.url.find("amazon.com") > -1:
        #    item.url = amazon.search(item.keywords)
        
        # get html for product page
        print(item.url)
        try:
            data = urllib.request.urlopen(item.url).read()
        except urllib.error.HTTPError as e:
            print("Error code: ", e.code)
            continue
        except urllib.error.URLError as e:
            print("Reason: ", e.reason)
            continue
        
        # look for text indicating that the item is sold out
        
        # if bestbuy.com url
        if item.url.find("bestbuy.com") > -1:
            sold_out = get_status_bestbuy(data)
        
        elif item.url.find("amazon.com") > -1:
            sold_out = get_status_amazon(data)
            
        else:
            print("unrecognized url: " + item.url)
        
        old_status = item.status
        item.set_status(sold_out)

        # only return items that are in stock and have not changed        
        if item.status == Status.IN_STOCK or item.status == Status.PRE_ORDER:
            if item.status != old_status:
                instock_items.append(item)
        
        time.sleep(1)
        
    return instock_items


def send_email(subject, text, html):
    """Send an email message using the settings in tracker.ini."""
    
    config = configparser.ConfigParser()
    config.read("tracker.ini")
    
    server = smtplib.SMTP(config["smtp"]["server"])
    server.ehlo()
    server.starttls()
    server.login(config["smtp"]["username"], config["smtp"]["password"])
    
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = config["message"]["from"]
    msg["To"] = config["message"]["to"]
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    msg.attach(part1)
    msg.attach(part2)
    
    server.sendmail(config["message"]["from"], config["message"]["to"], msg.as_string())
    server.quit()


def get_status_message(items):
    """Build stock status message using the given list of items."""
    
    msg = "Item Status\r\n"
    html = "<html><head></head><body><h1>Item Status</h1>"
    
    for item in items:
        
        msg += "\r\n\r\n"
        msg += item.name
        msg += "\r\n"
        msg += item.url
        msg += "\r\n"
        msg += "status: " + item.status.name
        
        html += "<div style=\"margin-top: 1em\"><p>" + item.name + "<br/>" + item.url + "<br/>"
        html += "status: " + item.status.name
        html += "</p></div>"
    
    html += "</body></html>"
    
    return msg, html


def main():
    
    items = get_items()
    
    while True:
        
        print("get_status - " + str(datetime.datetime.utcnow()))
        instock_items = get_status(items)
        
        if len(instock_items) > 0:
            
            # print the status of each url
            status_msg, status_html = get_status_message(instock_items)
            print(status_msg)
            
            send_email(
                "InStock Tracker - Item Status - " + str(datetime.datetime.utcnow()),
                status_msg, status_html)
        
        # sleep 5 minutes
        time.sleep(300)


if __name__ == "__main__":
    main()
