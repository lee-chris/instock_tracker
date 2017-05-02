from enum import Enum

class Status(Enum):
    
    UNKNOWN = -1
    SOLD_OUT = 0
    IN_STOCK = 1
    PRE_ORDER = 2

class Item(object):
    """Container object for each item to track.
    
    This object will store the basic attributes of the item as well as the in stock status.
    
    Attributes:
        name: user friendly name for the item
        url: url to the item page
        status: item status
    """
    
    def __init__(self, name, url):
        """Construct an Item object.
        
        Args:
            name: user friendly name for the item
            url: url to the item page
        """
        
        self.name = name
        self.url = url
        
        # abitrarily set to True here.
        # for the time being I don't want to take action if the item is sold out.
        self.status = Status.UNKNOWN
    
    
    def set_status(self, status):
        """Set the in stock status for this Item.
        
        Args:
            status: item status
        """
        
        self.status = status
