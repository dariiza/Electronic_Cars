import requests
import tkinter as tk
from bs4 import BeautifulSoup
from tabulate import tabulate
from tkinter import simpledialog

# definitions according to the website
URL = "https://www.carwow.de/elektroauto"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="page-template__body")

#GUI



def main():
    print("Unsorted car list")
    print("")
    car_list = get_car_list()
    print(tabulate(car_list, headers=["Name", "Ranking", "Price"]))
    print("")
    # chose "Name" to get the list sorted by name
    # "Price" to get it sorted by price
    # "Ranking" to get it sorted by ranking
    sort_list(USER_INP)



# function to print all cars on the website with information about name, price and ranking
def get_car_list():
    car_elements = results.find_all("div", class_="grid-container")
    car_list = []
    for car_element in car_elements:
        title_element = car_element.find("h3", class_="deal-review-highlight__title")
        if title_element is not None:
            end_number = title_element.text.find(".")
            title_element = str(title_element.text)
            title_element = title_element[end_number+1:]
        ranking_element = car_element.find("div", class_="deal-review-highlight__rating-text")
        price_element_raw = car_element('span')
        price_element = str(price_element_raw)
        end_span = price_element.find("(")
        if end_span != -1:
            price_element = price_element[end_span+1:15]
        else:
            end_span = price_element.find(">")
            price_element = price_element[end_span + 1:15]
        if not price_element_raw:
            price_element = "currently not Available"

        if title_element is not None and ranking_element is not None:
            car_list.append((title_element.strip(), ranking_element.text, price_element.strip()))
    car_list = list(dict.fromkeys(car_list))

    return car_list


# function to sort the list by a specific parameter
def sort_list(param):
    print("List sorted by " + param)
    print("")
    car_list = get_car_list()
    # sort the list according to the car name
    if param == "Name":
        sorted_by_name = sorted(car_list, key=lambda tup: tup[0])
        print(tabulate(sorted_by_name))
    elif param == "Ranking":
        sorted_by_ranking = sorted(car_list, key=lambda tup: tup[1], reverse=True)
        print(tabulate(sorted_by_ranking))
    elif param == "Price":
        sorted_by_price = sorted(car_list, key=lambda tup: tup[2])
        print(tabulate(sorted_by_price, headers=["Name", "Ranking", "Price"]))


ROOT = tk.Tk()

ROOT.withdraw()
USER_INP = simpledialog.askstring(title="GUI",
                                  prompt="Sort list by:(Name, Ranking, Price)")



main()


