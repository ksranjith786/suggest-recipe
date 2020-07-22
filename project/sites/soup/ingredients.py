from bs4 import BeautifulSoup
import requests

#URL = 'https://hebbarskitchen.com/plain-dosa/'
class IngredientsExtractor:
    def __init__(self, URL):
        self.URL = URL
        self.TITLE = ""
        self.INGREDIENTS = []
        self.soupObj = None
        
    def getResponse(self):
        return requests.get(self.URL).text
    
    def scrapeURL(self):
        data = self.getResponse()
        self.soupObj = BeautifulSoup(data, 'html.parser')

    def getTitle(self):
        if self.soupObj == None:
            self.scrapeURL()
        
        self.TITLE = self.soupObj.title.text
        return self.TITLE

    def getImageUrl(self):
        if self.soupObj == None:
            self.scrapeURL()

        soup = self.soupObj
        for div in soup.find_all('div', {'class': "wprm-recipe-container"}):
            for image_div in div.findAll('div', {'class': "wprm-recipe-image"}):
                for image_link in image_div.findAll('img'):
                    self.IMAGE_URL = image_link.get('data-lazy-src')
                    #print(image_link.get('data-lazy-src')) #print(image_link.get('src'))
                    break
                break
            break
        
        return self.IMAGE_URL

    def getIngredients(self):
        if self.soupObj == None:
            self.scrapeURL()
        
        soup = self.soupObj
        for div in soup.find_all('div', {'class': "wprm-recipe-container"}):
            for div in div.find_all('div', {'class': "wprm-recipe-ingredient-group"}):
                #print(div.text)
                for list_item in div.findAll('li', {'class': "wprm-recipe-ingredient"}):
                    self.INGREDIENTS.append(list_item.text)
        
        return self.INGREDIENTS

    # For call to repr(). Prints object's information 
    def __str__(self):
        return '%s (%s, %s, %s)' % (self.__class__, self.TITLE, self.IMAGE_URL, self.INGREDIENTS)
    
# end class

if __name__ == "__main__":
    URL = 'https://hebbarskitchen.com/plain-dosa/'
    extractor = IngredientsExtractor(URL)
    #extractor.getTitle()
    #extractor.getImageUrl()
    #extractor.getIngredients()
    #print(str(extractor))
    #print(repr(extractor))
    #print(extractor)
