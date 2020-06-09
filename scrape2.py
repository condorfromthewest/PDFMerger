from bs4 import BeautifulSoup
import requests
import pandas as pd
import time 

def custom_feed_single():
    ''' This function runs a single scrape just for the homepage, collecting items in a dictionary 
    and storing them in a list, extracting the title, link and votes information.
    '''
    custom_list = []
    res = requests.get(f'https://news.ycombinator.com/')
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.find_all(class_='storylink')
    point_count = soup.find_all(class_='score')
    for count, article in enumerate(articles):
        title = article.text
        link = article['href']
        points = int(point_count[count - 1].text.split(' ')[0])
        custom_list.append({'Title': title, 'Link': link, 'Votes': points})
    return sorted_pd(custom_list)

def custom_feed_various(pages):
    ''' Multi page scraper which scans the number of pages indicated by the user at the beginning 
    of script execution. Collects items in a dictionary and stores them in a list, 
    extracting the title, link and votes information.
    '''
    custom_list = []
    for i in range(pages):
        res_pages = requests.get(f'https://news.ycombinator.com/news?p={i+1}')
        soup = BeautifulSoup(res_pages.text, 'html.parser')
        articles = soup.find_all(class_='storylink')
        point_count = soup.find_all(class_='score')
        print(f'Scraping page {i+1}...')

        for count, article in enumerate(articles):
            title = article.text
            link = article['href']
            points = int(point_count[count-1].text.split(' ')[0])
            custom_list.append({'Title': title, 'Link': link, 'Votes': points})
    return sorted_pd(custom_list)

def sorted_pd(list):
    ''' Grabs the article list created in the single or multi page scraper and converts it into a 
    Pandas dataframe for easy reading and manipulation. The user inputs the desired
    points score for further filtering.
    '''
    df = pd.DataFrame(list)
    df = df.sort_values(['Votes'], ascending=False)
    p = int(input('Please enter your points filter: '))
    time.sleep(1)
    print('and... All done!')
    time.sleep(1)
    print('Here is your custom selection: ')
    time.sleep(1)
    return df[df['Votes']>p]

def run_scrape():
    '''Script execution which promps the user to select how many pages to scrape and whether to display
    full or just top 5 results.
    '''
    n = int(input('How many pages do you wish to scrape? '))
    q = input('For complete results, type "all". For just the top 5, type "head": ')
    if n >= 2:
        if q == 'all':
            print(custom_feed_various(n))
        elif q == 'head':
            print('Here are your 5 most popular articles: ')
            print(custom_feed_various(n).head())
    elif n ==1:
        if q == 'all':
            print(custom_feed_single())
        elif q == 'head':
            print('Here are your 5 most popular articles: ')
            print(custom_feed_single().head())

run_scrape()
