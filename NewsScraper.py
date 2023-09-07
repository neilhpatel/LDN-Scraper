import requests
from bs4 import BeautifulSoup
from datetime import date
import urllib.request


class NewsScraper:

    def __init__(self, inputDate):
        self.homePage = "https://www.lagrangenews.com"
        self.dateToParseURLs = inputDate

    """
    Parse through the html of a url and add all paragraph text 
    """
    def parseArticle(self, url):
        html = urllib.request.urlopen(url)
        htmlParse = BeautifulSoup(html, 'html.parser')
        txt = []
        i = 0
        for para in htmlParse.find_all("p"):
            if i != 0 and i != 1:
                txt.append(para.get_text())
            i += 1
        return txt

    """
    Parse through the html of a url and find the title of the article  
    """
    def retrieveTitle(self, url):
        html = urllib.request.urlopen(url)
        htmlParse = BeautifulSoup(html, 'html.parser')
        title = None
        for tag in htmlParse.find_all('h2', class_="headline"):
            title = tag.get_text()

        return title

    """
    Convert the mapping of title to article content into a single properly formatted string which will be sent via email
    """
    def convertArticlesIntoMessage(self, articles):
        output = ""
        number = 1
        for k, v in articles.items():
            output += f"Article {number}: {k}"
            output += "\n"
            output += ''.join(v)
            output += "\n\n\n"
            number += 1

        return output

    """
    Read the home page of Lagrange Daily News and scrape all URLs containing the date self.dateToParseURLs.
    """
    def readHomePage(self):
        try:
            request = requests.get(self.homePage)
            soup = BeautifulSoup(request.text, 'html.parser')
        except:
            print("Could not scrape data from LDN. Exiting")
            return

        urls = set()
        for link in soup.find_all('a'):
            url = link.get('href')
            if self.dateToParseURLs in url:
                urls.add(url)

        articles = {}
        for url in urls:
            title = self.retrieveTitle(url)
            text = self.parseArticle(url)
            if not title:
                "Could not find a title for url " + str(url)
                continue
            articles[title] = text

        if not articles:
            return None

        formattedArticles = self.convertArticlesIntoMessage(articles)


        return formattedArticles


