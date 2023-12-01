from bs4 import BeautifulSoup


def search_data(responce):
    soup = BeautifulSoup(responce.text, "html.parser")
    a, b, c = None, None, None
    if soup.find('h1'):
        a = soup.find('h1').text
    if soup.find('title'):
        b = soup.find('title').text
    for x in soup.find_all('meta'):
        if x.get('name') == 'description':
            c = x.get('content')
    return a, b, c
