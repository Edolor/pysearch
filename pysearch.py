"""pip search --name replacement."""
import re
import sys
from urllib.request import urlopen
from urllib.error import HTTPError 
from urllib.error import URLError
from bs4 import BeautifulSoup

class Pip():
    """Modelling pip search functionality, prints first three pages of a search result."""
    page_no = 1
    
    def __init__(self, query):
        """Setting attributes."""
        self.url = "https://pypi.org/search/?q=" + query

    def get_url(self, url):
        """Return None or a Beautifull soup object given a URL."""
        soup = None

        try:
            html = urlopen(url, timeout=5)
        except URLError as e:
            print(e)
        except HTTPError as e:
            print(e)
        except ValueError as e:
            print(e)
        else:
            soup = BeautifulSoup(html.read(), "html.parser")
            return soup

        return None
    
    def increase_page(self):
        """increment the page number."""
        Pip.page_no = Pip.page_no + 1
        self.url += f"&page={Pip.page_no}"
        
    def elements(self, url):
        """Returns none if no results is found else, returns a list of tags."""
        
        tags = [] # Holds search result tags.
        soup = self.get_url(url)

        if soup:
            tags = soup.find_all("a", href=re.compile(r"^(/project.+)"))
            if tags:
                try: # Checking for empty pages.
                    items = []
                    counter = 0
                    while counter < len(tags): # Searching each link, for names.
                        tag = tags[counter].h3.find_all("span", class_=re.compile("^package-snippet*"))
                        tag.append(tags[counter].p)
                        items.append(tag)
                        counter += 1

                    return items

                except AttributeError:
                    pass
                else:
                    return items
            else:
                return None # Page does not exist
            return tags # May return None if it finds no tags.
        else:
            return None
   
    def extract_info(self, tags):
        """Returns None for empty page, returns dictionary if tag found"""
        details = [] # Returns a list of results. 

        for tagss in tags:
            items = []
            counter = 0
            while counter < len(tagss):
                items.append(tagss[counter].get_text().strip())
                counter += 1
            details.append(items)

        return details
    
    def display(self, search):
        """Displays individual searches"""
        name = search[0]
        version = search[1]
        date = search[2]
        description = search[3]
        print("Name: " + name)
        print("Version: " + version)
        print("Date: " + date)
        print("Description: " + description)
        print()


def get_input(query):
    """Convert user request to a search query parameter."""
    
    if query:
        # Search for space in the user query.
        temp_regex = re.compile(r"\s")
        query = temp_regex.sub("+", query)
        return query
    else:
        return None

def main():
    """Displays first 3 pages of a search query if found."""
    result = Pip(query) # Pip object.
    print("\n")
    end_page = 4
    
    while result.page_no != end_page: #First three pages
        tags = result.elements(result.url) # Returns first page of search.
        if tags: 
            searches = result.extract_info(tags) # Check if links are present.
            if searches: # Extracting all elements>
                for search in searches: # Extracting individual elements.
                    result.display(search) # Displaying results.
            result.increase_page()
            if result.page_no != end_page:
                print("-" * 20)
                print(f"Page {Pip.page_no}")
                print("-" * 20, end="\n\n")
        else:
            if result.page_no != 1:
                print("End of file") # If page is not available then display this
                break

            print("Nothing was found.")

if len(sys.argv) < 2:
    query = input("Enter package to search: ")
    query = get_input(query)
    
    if query:
        main()
    else:
        print("Invalid query entered.")

else:
    query = sys.argv[1]
    query = get_input(query)
   
    # if user query passes.
    if query:
        main()
    else:
        print("Invalid query entered.")


