from bs4 import BeautifulSoup
import requests

#URL = 'https://hebbarskitchen.com/plain-dosa/'
class IngredientsExtractor:
    def __init__(self, url, provider=""):
        self.URL = url
        self.NAME = ""
        self.INGREDIENTS = []
        self.TYPE = ""
        self.IMAGE_URL = ""
        self.PROVIDER = provider

        self.soupObj = None
        
    def getResponse(self):
        return requests.get(self.URL).text
    
    def scrapeURL(self):
        data = self.getResponse()
        self.soupObj = BeautifulSoup(data, 'html.parser')

    def getName(self):
        if self.soupObj == None:
            self.scrapeURL()
        
        self.NAME = self.soupObj.title.text
        return self.NAME
    
    def getUrl(self):
        return self.URL

    def getType(self):
        if self.soupObj == None:
            self.scrapeURL()

        soup = self.soupObj
        for meta in soup.find_all('meta', {'property': "article:section"}):
            self.TYPE = meta['content']
        
        return self.TYPE

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
                    value = list_item.text.replace("▢", "").strip()
                    # print(f'getIngredients: list_item: {list_item.text} and value: {value}')
                    self.INGREDIENTS.append(value)
        
        return self.INGREDIENTS

    def getProvider(self):
        return self.PROVIDER

    # For call to repr(). Prints object's information 
    def __str__(self):
        return '%s (%s, %s, %s, %s, %s)' % (self.__class__, self.URL, self.NAME, self.TYPE, self.IMAGE_URL, self.INGREDIENTS)
    
# end class

if __name__ == "__main__":
    URL = 'https://hebbarskitchen.com/plain-dosa/'
    extractor = IngredientsExtractor(URL)
    #extractor.getNAME()
    #extractor.getImageUrl()
    #extractor.getIngredients()
    #print(str(extractor))
    #print(repr(extractor))
    #print(extractor)
