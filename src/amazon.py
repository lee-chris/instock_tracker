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

"""
if __name__ == "__main__":
    search("Breath of the Wild Zelda amiibo")
"""
