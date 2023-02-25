import requests, time
from bs4 import BeautifulSoup
from requests import RequestException

ITEMS = 100

# Set headers to be used in requests
headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'qzip, deflate, br',
    'Connection': 'keep-alive'
}


# Extract the maximum page number from the search results
def extract_max_page(url):
    # Send a GET request to the provided URL with the headers
    hh_request = requests.get(url, headers=headers, allow_redirects=False)
    # Create a BeautifulSoup object from the HTML response
    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')
    pages = []
    # Find all the page number elements
    paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})
    # Extract the integer value of the page numbers and append them to the `pages` list
    for page in paginator:
        pages.append(int(page.find('a').text))
        # Return the last page number in the `pages` list
    return (pages[-1])


# Extract job information from a HTML element
def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
    company = company.strip()
    company = company.replace(u'\xa0', u' ')
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.partition(',')[0]
    return {'title': title, 'company': company, 'location': location, 'link': link}


# Extract job information from all the pages in the search results
def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f'Parsing page {page}')
        result = None
        # Make the request until it succeeds, with a delay between retries
        while result is None:
            try:
                # Send a GET request to the provided URL with the headers and page number
                result = requests.get(f'{url}&page={page}', headers=headers, timeout=10, allow_redirects=False)
            except RequestException:
                # If the request fails, print a message and wait 5 seconds before retrying
                print('Request failed, waiting and trying again...')
                time.sleep(5)
        # Create a BeautifulSoup object from the HTML response
        soup = BeautifulSoup(result.text, 'html.parser')
        # Find all the job elements
        results = soup.find_all('div', {'class': 'serp-item'})
        # Extract the job information and append it to the `jobs` list
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


# Perform a search for jobs on hh.ru with the provided keyword
def get_jobs(keyword):
    url = f'https://hh.ru/search/vacancy?st=searchVacancy&text={keyword}&items_on_page={ITEMS}'
    max_page = extract_max_page(url)
    jobs = extract_jobs(max_page, url)
    return jobs
