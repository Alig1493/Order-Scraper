import re

import pandas

from decouple import config
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup


def get_value_or_none(element):
    try:
        return element.text
    except AttributeError:
        return ""


def two_factor_bypass(driver, key):
    try:
        driver.find_element_by_css_selector("input#approvals_code").send_keys(key)
        driver.find_element_by_css_selector("button#checkpointSubmitButton").click()

        driver.find_element_by_css_selector("input[id^='u_0_'][value='dont_save']").click()
        driver.find_element_by_css_selector("button#checkpointSubmitButton").click()

        driver.find_element_by_css_selector("button#checkpointSubmitButton").click()

        driver.find_element_by_css_selector("button#checkpointSubmitButton").click()

        driver.find_element_by_css_selector("input[id^='u_0_'][value='dont_save']").click()
        driver.find_element_by_css_selector("button#checkpointSubmitButton").click()

    except NoSuchElementException:
        pass


def main():
    email = config("EMAIL", default="")
    password = config("PASSWORD", default="")

    driver = webdriver.Firefox()
    # Navigate to facebook to login first before going to group since it requires authentication especially for a closed group
    driver.get("https://www.facebook.com/")

    driver.find_element_by_css_selector("input#email").send_keys(email)
    driver.find_element_by_css_selector("input#pass").send_keys(password)
    driver.find_element_by_css_selector("input[id^='u_0_'][value='Log In']").click()

    # in case your facebook is protected by two factor authentication, otherwise you can comment it out
    # please input your google two factor generated key if you have one besides the key variable inside the function
    two_factor_bypass(driver=driver, key="167242")

    orders_list = []

    driver.get("https://www.facebook.com/groups/cookupsBD/")
    html_page = driver.page_source
    soup = BeautifulSoup(html_page, features="html.parser")

    elements = soup.find_all("div", class_="_5pcr userContentWrapper", limit=100)

    # skip the first item since it's basically an admin pinned post and not a sale post
    for element in elements[1:]:
        name = get_value_or_none(element.find("span", class_="fwb").find_next("a"))
        print(name)
        post_time = get_value_or_none(element.find("span", class_="timestampContent"))
        print(post_time)

        detail_element = element.find("div", class_="mtm")
        order_title = get_value_or_none(detail_element.find("div", class_="_l53"))
        print(order_title)
        order_price = get_value_or_none(detail_element.find("div", class_="_l57"))
        print(order_price)
        order_location = get_value_or_none(detail_element.find("div", class_="_l58"))
        print(order_location)

        text_list = []
        link_list = []

        # print(detail_element.prettify())
        more_detail = detail_element.find("div", class_="userContent").find_all("p")
        for para in more_detail:
            text = get_value_or_none(para)
            # print(text)
            text_list.append(text)
            link = para.find_all("a")
            if link:
                for l in link:
                    l_value = get_value_or_none(l)
                    # print("Link: ", l_value)
                    link_list.append(l_value)

        text_body = "".join(text_list)
        link_body = ", ".join(link_list)

        print("Description: ", text_body)
        print("Links: ", link_body)

        next_detail_element = detail_element.find_next_sibling("div", class_="mtm")
        image_element = next_detail_element.find("img", class_="scaledImageFitWidth")
        image_link = ""
        if image_element:
            image_link = image_element["src"]
        # print(next_detail_element.prettify())
        print(image_link)
        # print([detail.find("a").text for detail in more_detail])
        order_dict = {
            "name": name,
            "time": post_time,
            "title": order_title,
            "price": order_price,
            "location": order_location,
            "description": text_body,
            "links": link_body,
            "image": image_link
        }
        orders_list.append(order_dict)
        print("=====================================================================================================================================")
		
		# Output in Excel Sheet
        dataframe = pandas.DataFrame(orders_list)
        writer = pandas.ExcelWriter('Cookups Order.xlsx')
        dataframe.to_excel(writer)
        writer.save()


if __name__ == "__main__":
    main()
