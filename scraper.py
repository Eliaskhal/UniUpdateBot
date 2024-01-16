import requests
from bs4 import BeautifulSoup
import csv

file_path = 'Date Tracker.csv'

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            return row
        
def write_csv_date(file_path, new_date):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_date])

def check_date(date1, date2):
    if date1[0]>date2[0] or (date1[0]==date2[0] and date1[1]>date2[1]) or (date1[0]==date2[0] and date1[1]==date2[1] and date1[2]>date2[2]): return True
    else: return False

def scrape_uni_website(old_date:list[str]):
    global content, attachments
    base_url = 'https://www.est-umi.ac.ma/'
    url = base_url + 'actualite.php'
    response = requests.get(url)


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('h5', class_='event-title')


        for article in articles:
            date_str = article.find_previous('span', class_='event-place').text.strip()
            title = article.find('a').text

            date = date_str.split('-')

            if check_date(date, old_date):
                article_link = article.find('a')['href']

                article_response = requests.get(base_url + article_link)
                article_response.raise_for_status()  

                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    content_p = article_soup.find('div', class_='blog-post-inner').find('p')
                    content = content_p.text.strip() if content_p else 'None'

                    attachments = article_soup.find_all('a', rel='tag')

                process_and_store_article(title, date_str, content, attachments)
        write_csv_date(file_path, articles[0].find_previous('span', class_='event-place').text.strip())


def process_and_store_article(title, date_str, content, attachments):
    encoded_title = title.encode('utf-8').decode('utf-8').title()

    print(f"Date: {date_str}, Title: {encoded_title}")
    print(f"Content: {content}")

    for attachment in attachments:
        attachment_name = attachment.text
        attachment_link = 'https://www.est-umi.ac.ma/'+attachment['href']
        print(f"Attachment: {attachment_name} - {attachment_link}")
    print()

    # attachment_id = ', '.join([attachement['href'].split('/')[-1] for attachement in attachments])
    # attachement_links = ['https://www.est-umi.ac.ma/'+attachment['href'] for attachment in attachments]

parsed_date = read_csv_file(file_path)[-1].split('-')

if __name__ == "__main__":
    scrape_uni_website(parsed_date)