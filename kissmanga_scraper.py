import time
import re
import requests
from multiprocessing.pool import ThreadPool as Pool
from bs4 import BeautifulSoup

class KissmangaScraper:
    def get_soup(self, url):
        """Scrape content from url and parse it using BeautifulSoup.
        """
        
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_manga_list(self):
        """Get manga list from Kissmanga.
        """
        
        result = []
        next_link = 'http://kissmanga.com/MangaList'

        while next_link is not '': 
            soup = self.get_soup(next_link)
            mangas = soup.find('table', class_='listing').find_all('tr')
            for manga in mangas:
                link = manga.find('a')
                if link is not None :
                    link = str(link['href'].encode('utf-8'))
                    link = 'http://kissmanga.com' + link[2:-1]
                    result[len(result):] = [link]

            pagers = soup.find(class_='pagination').find_all('a')
            next_link = ''
            for pager in pagers:
                if re.search('Next', str(pager.get_text().encode('utf-8'))):
                    next_link = str(pager['href'].encode('utf-8'))
                    next_link = 'http://kissmanga.com' + next_link[2:-1]

        return result


    def get_chapter_list(self, url):
        """Get chapter list of a manga.
        """

        result = []
        if url is '':
            return result

        soup = self.get_soup(url)
        chapters = soup.find('table', class_='listing').find_all('a')
        for link in chapters:
            if link is not None :
                link = str(link['href'].encode('utf-8'))
                link = 'http://kissmanga.com' + link[2:-1]
                result[len(result):] = [link]

        return result

    def get_images(self, url):
        """Get images from a chapter.
        """

        result = []
        if url is '':
            return result

        soup = self.get_soup(url)
        scripts = soup.find_all('script')
        for script in scripts:
            if re.search('lstImages.push', script.get_text()):
                p = re.compile('lstImages.push\("(.*)"\)')
                pages = p.findall(script.get_text())
                result = pages
                break

        return result


# get_manga_list()
# get_chapter_list('http://kissmanga.com/Manga/Onepunch-Man-ONE')
# get_images('http://kissmanga.com/Manga/Ayeshah-s-Secret/Vol-001-Ch-001-Read-Online?id=241934')

if __name__ == '__main__':
    print('Started')

    start = time.time()
    scraper = KissmangaScraper()
    urls = scraper.get_chapter_list('http://kissmanga.com/Manga/Onepunch-Man-ONE')    
    print(str(len(urls)) + ' chapters found')

    img_count = 0
    results = []
    
    # With parallel processing
    # pool = Pool(8)
    # results = pool.map(scraper.get_images, urls)

    # Without parallel processing
    for url in urls:
        results[len(results):] = [scraper.get_images(url)]

    for img in results:
        img_count += len(img)

    print(str(img_count) + ' images found')

    end = time.time()
    elapsed = end - start
    print('Finished in ' + str(elapsed) + ' seconds')