from flask import Blueprint, request
from sites.soup.findSites import run

management_bp = Blueprint('management', __name__, url_prefix='/management')

@management_bp.route('/data/scrape', methods=['GET'])
def scrapeSite():
    provider = request.args.get('provider', type=str)
    url = request.args.get('url', type=str)
    #print(provider, url)
    retVal = run(url, provider)
    msg = "Scraping Data from " + provider + " is successful"
    if retVal is False:
        return "Failed to scrape Data from " + provider

    return msg
# end scrapeSite
