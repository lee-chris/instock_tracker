class Item(object):
    """Container object for each item to track.
    
    This object will store the basic attributes of the item as well as the in stock status.
    
    Attributes:
        name: user friendly name for the item
        url: url to the item page
        sold_out: boolean flag to indicate that the item is sold out (true means sold out)
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
        self.sold_out = True
    
    
    def set_status(self, sold_out):
        """Set the in stock status for this Item.
        
        Args:
            sold_out: boolean flag to indicate that the item is sold out
        """
        
        self.sold_out = sold_out
