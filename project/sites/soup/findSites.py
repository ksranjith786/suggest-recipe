import requests
from bs4 import BeautifulSoup
from ingredients import IngredientsExtractor

URL='https://hebbarskitchen.com'
url_response = requests.get(URL).text
main_soup = BeautifulSoup(url_response, 'html.parser')

RECIPE_LINK=''
#for link in soup.find_all('a'):
#    print(link.get('href'))

"""
# Get the links that matches 'recipes'
for link in soup.find_all('a'):
    link_href = link.get('href')
    if "recipes" in link_href:
        print(link_href)
"""
# Header Wrap
#td-header-menu-wrap-full td-container-wrap 
MENU_URL_LIST= dict()
for div_header in main_soup.find_all('div', {'id': 'td-header-menu'}):
    #print('Div Header')
    for div in div_header.findAll('div', {'class': 'menu-new-right-menu-container'}):
        #print('Div')
        for list_item in div.findAll('li', {'class': 'menu-item-has-children'}):
            #print('List Item')
            #print(list_item.text)
            for link in list_item.findAll('a'):
                #print('Link')
                #print(link.get('href'))
                name = ""
                for list_name in list_item.select_one('a'):
                    name = list_name

                MENU_URL_LIST[name] = link.get('href')
                break
        #print a.text.strip(), '=>', a.attrs['href']
    #print(header_link.get('href'))

#for k,v in MENU_URL_LIST.items():
#    print(f'{k} => {v}')

for SUB_URL in MENU_URL_LIST.values():
    sub_url_response = requests.get(SUB_URL).text
    sub_soup = BeautifulSoup(sub_url_response, 'html.parser')
    
    # Get the no.of pages
    for div in sub_soup('div', {'class': "page-nav td-pb-padding-side"}):
        last_page = 1
        for link in sub_soup.find_all('a', {'class':"last"}):
            last_page = int(link.text)
            #print(link.get('href'))
    # Go through each page
    for page_num in range(1, last_page + 1):
        PAGE_URL = SUB_URL + 'page/' + str(page_num)
        page_url_response = requests.get(PAGE_URL).text
        page_soup = BeautifulSoup(page_url_response, 'html.parser')
        print(page_num, "/", last_page)
        # Get the recipe links
        for link in page_soup.find_all('a', {'class':"td-image-wrap"}):
            RECIPE_LINK = link.get('href')
            print(RECIPE_LINK)
            ingredientsExt = IngredientsExtractor(RECIPE_LINK)
            ingredientsExt.getTitle()
            ingredientsExt.getImageUrl()
            ingredientsExt.getIngredients()
            print(ingredientsExt)

            break
        break
    break

#for item in soup.find_all(attr={"class": "td-item-details"}):
#    print(item)
