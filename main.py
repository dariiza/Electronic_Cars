import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

URL = "https://www.carwow.de/elektroauto"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="page-template__body")

car_elements = results.find_all("div", class_="grid-container")
car_list = []

for car_element in car_elements:
    title_element = car_element.find("h3", class_="deal-review-highlight__title")
    if title_element != None:
        end_number = title_element.text.find(".")
        title_element = str(title_element.text)
        title_element = title_element[end_number+1:]
    ranking_element = car_element.find("div",class_= "deal-review-highlight__rating-text")
    price_element_raw = car_element('span')
    price_element = str(price_element_raw)
    end_span = price_element.find("(")
    if end_span != -1:
        price_element = price_element[end_span+1:15]
    else:
        end_span = price_element.find(">")
        price_element = price_element[end_span + 1:15]

    if title_element != None and ranking_element != None :
        car_list.append((title_element, ranking_element.text, price_element))

car_list = list(dict.fromkeys(car_list))

print(tabulate(car_list))

