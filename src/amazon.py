import urllib.request

def search(search_term):
    """Execute a search on amazon and return the url for the first search result.
    
    The expected behavior here is similar to the I'm feeling lucky Google search.
    If there are no search results, then an empty string is returned.
    
    Args:
        search_term: search term for the query
    """
    
    search_url = "https://www.amazon.com/s/?field-keywords=" + str(search_term).replace(" ", "+")
    html = str(urllib.request.urlopen(search_url).read())
    
    # find the search results list
    ul_start = html.find("<ul id=\"s-results-list-atf\"")
    
    # ul_end = html.find("</ul>", ul_start + 1)
    # print(html[ul_start:ul_end])
    
    # if there are no search results
    if ul_start == -1:
        return ""
    
    # find the first search result
    li_start = html.find("<li id=\"result_0\"", ul_start)
    
    # if there are no search results
    if li_start == -1:
        return ""
    
    # find the anchor element of the first result
    a_start = html.find("s-access-detail-page", li_start)
    
    # extract the href from the anchor
    href_start = html.find("href=\"", a_start)
    href_end = html.find("\"", href_start + 6)
    
    result_url = html[href_start + 6:href_end]
    
    return result_url


def search_all(search_term):
    """Search amazon and parse the results"""
    
    # I'm not sure if this is the best way or not, instead of parsing each product page individually.
    
    search_url = "https://www.amazon.com/s/?field-keywords=" + str(search_term).replace(" ", "+")
    html = str(urllib.request.urlopen(search_url).read())
    
    # find the search results list
    ul_start = html.find("<ul id=\"s-results-list-atf\"")
    
    # ul_end = html.find("</ul>", ul_start + 1)
    # print(html[ul_start:ul_end])
    
    i = html.find("<li id=\"result_", ul_start)
    
    while i != -1:
        
        li_end = html.find("</li>", i)
        
        # find the main link to the product page
        a_detail_page_start = html.find("s-access-detail-page", i)
        
        # extract product name from this element
        title_start = html.find("title=\"", a_detail_page_start)
        title_end = html.find("\"", title_start + 7)
        
        item_name = html[title_start + 7:title_end]
        
        # extract url from this element
        href_start = html.find("href=\"", a_detail_page_start)
        href_end = html.find("\"", href_start + 6)
        
        item_url = html[href_start + 6:href_end]
        
        # find the price displayed for this search result
        span_price_large = html.find("sx-price-large", i, li_end)
        
        if span_price_large != -1:
            
            price_label_start = html.rfind("aria-label=\"", i, span_price_large)
            price_label_end = html.find("\"", price_label_start + 12)
            
            item_price = html[price_label_start + 12:price_label_end]
            
        else:
            
            item_price = -1
        
        # debugging output
        print(item_name)
        print(item_url)
        print(item_price)
        print("\n")
        
        # proceed to next search result
        i = html.find("<li id=\"result_", i + 1)


"""
if __name__ == "__main__":
    search_all("Breath of the Wild Zelda amiibo")
"""

