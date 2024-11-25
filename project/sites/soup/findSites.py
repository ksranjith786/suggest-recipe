import requests
from bs4 import BeautifulSoup

from sites.soup.ingredients import IngredientsExtractor
from database.database import addRecipeToDB

def run(url, provider):
    print(f'URL: {url} Provider: {provider}')

    url_response = None
    main_soup = None

    try:
        url_response = requests.get(url).text
        main_soup = BeautifulSoup(url_response, 'html.parser')
    except Exception as e:
        print("Exception caught while retrieving data from website. Error: ", e)
        return False
    
    # for link in main_soup.find_all('a'):
    #    print(link.get('href'))

    """
    # Get the links that matches 'recipes'
    for link in main_soup.find_all('a'):
        link_href = link.get('href')
        if "recipes" in link_href:
            print(link_href)
    """
    # Browse by Category
    BROWSE_BY_CATEGORIES = dict()
    for div_cat in main_soup.find_all('div', {'class': "menu-new-right-menu-container"}):
        # print(f'Div Category: {div_cat}')
        for ul in div_cat.findAll('ul', {'class': "td-mobile-main-menu"}):
            # print(f'\n***\nul: {ul}')
            for list_item in ul.findAll('li', {'class': "menu-item-has-children"}):
                for sub_list_item in list_item.findAll('li', {'class': "menu-item"}):
                    # print(f'\n***\nList Item: {sub_list_item.text}')
                    for link in sub_list_item.findAll('a'):
                        # print(f'\n***\nLink: {link.get('href')}')
                        name = ""
                        for list_name in sub_list_item.select_one('a'):
                            name = list_name

                        BROWSE_BY_CATEGORIES[name] = link.get('href')
                        break
                    #print a.text.strip(), '=>', a.attrs['href']

    # print("\n*** Links from Browse By Categories, Size:", len(BROWSE_BY_CATEGORIES))
    # for k,v in BROWSE_BY_CATEGORIES.items():
    #     print(f'{k} => {v}')
    
    RECIPE_LINKS = dict()
    RECIPE_PAGES = [page for page in BROWSE_BY_CATEGORIES.values()]
    RECIPE_PAGES.append("https://hebbarskitchen.com/recipes/top-paneer-recipes-paneer-curries")
    # print("Fetching Recipe Pages")
    for PAGE_URL in RECIPE_PAGES:
        page_url_response = None
        page_soup = None

        try:
            page_url_response = requests.get(PAGE_URL).text
            page_soup = BeautifulSoup(page_url_response, 'html.parser')
        except Exception as e:
            print("Exception caught while retrieving data from website. Error: ", e)
            return False
        # Get the Recipe Links from this page
        # print(f'PAGE_URL: {PAGE_URL}')
        for div_con in page_soup.find_all('div', {'class': "td-block-span6"}):
            # print(f'Div Category: {div_con.text}')
            for link in div_con.findAll('a', {'class':"td-image-wrap"}):
                RECIPE_NAME = link.get('title')
                RECIPE_LINK = link.get('href')
                RECIPE_LINKS[RECIPE_NAME] = RECIPE_LINK
            # end for link
        # end for div_con

        # Get recipe pages
        for div_nav in page_soup('div', {'class': "page-nav td-pb-padding-side"}):
            for link in div_nav.find_all('a', {'class': "page"}):
                NEXT_PAGE = link.get('href')
                # As there are PREVIOUS and NEXT buttons with out class <a>; let's skip if the previous link exists already
                if NEXT_PAGE in RECIPE_PAGES:
                    continue
                
                RECIPE_PAGES.append(NEXT_PAGE)
                # print(NEXT_PAGE)
            # end for link
        # end for div_nav
    # end for PAGE_URL

    print("No.of recipe links:", len(RECIPE_LINKS))
    # print(RECIPE_LINKS)
    print("Fetching Recipe Links")
    for RECIPE_LINK in RECIPE_LINKS.values():
        ingredientsExt = IngredientsExtractor(RECIPE_LINK, provider)
        name = ingredientsExt.getName()
        url = ingredientsExt.getUrl()
        type = ingredientsExt.getType()
        imageURL = ingredientsExt.getImageUrl()
        ingredients = ingredientsExt.getIngredients()

        # Check whether ingredients are empty then skip adding to database
        if len(ingredients) == 0:
            print(RECIPE_LINK, "[Skipped]")
            continue
        else:
            print(RECIPE_LINK)
            # Continue adding to Database
            retVal = addRecipeToDB(
                    name = name,
                    url = url,
                    type = type,
                    imageURL = imageURL,
                    ingredients = str(ingredients), # Converting list to string
                    provider = provider
                )
            if retVal == False:
                print("Exception caught while adding recipe details to Database")
                return False
            # end if retVal
        # end if len
    # end for RECIPE_LINK

    return True

if __name__ == "__main__":
    url = ""
    provider = ""

    run(url, provider)
