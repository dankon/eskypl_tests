#-*- coding: utf-8 -*-
#!/usr/bin/env python
"""
This is a simple script for tests esky.pl website functionality 
by Selenium/Webdriver Python module.
"""
from datetime import date
from time import sleep

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

MONTHS_PL = {1 : u"styczeń",   
             2 : u"luty",
             3 : u"marzec",
             4 : u"kwiecień", 
             5 : u"maj",
             6 : u"czerwiec",
             7 : u"lipiec",
             8 : u"sierpień",
             9 : u"wrzesień",
             10 : u"październik",
             11 : u"listopad",
             12 : u"grudzień"
            }

def click_date_on_calendar(calendar_div, dt_date):
    """
    Function for click date on pop up calendar.
    Params:
    # calendar_div - html div contain pop up calendar
    # dt_date - datetime instance of date
    """
    calendar_year = calendar_div.find_element_by_css_selector("span.ui-datepicker-year").text
    calendar_month = calendar_div.find_element_by_css_selector("span.ui-datepicker-month").text
    while not (calendar_month.lower() == MONTHS_PL[dt_date.month]\
               and int(calendar_year) == dt_date.year):
        calendar_div.find_element_by_xpath("./div/a[@data-handler='next']").click()
        sleep(1)
        calendar_year = calendar_div.find_element_by_css_selector("span.ui-datepicker-year").text
        calendar_month = calendar_div.find_element_by_css_selector("span.ui-datepicker-month").text
    for link in  calendar_div.find_elements_by_xpath('./table/tbody/tr/td/a'):
        if int(link.text) == dt_date.day:
            link.click()
            break


def fill_flights_form(flights_form, departure, arrival, dep_date):
    """
    Function for fill up flights form.
    With departure, arrival and departure date (dep_date) as params.
    Return date is equal to departure date plus 3 months.
    """
    departure_input = flights_form.find_element_by_id("departureRoundtrip0")
    departure_input.clear()
    departure_input.send_keys(departure)
    arrival_input = flights_form.find_element_by_id("arrivalRoundtrip0")
    arrival_input.clear()
    arrival_input.send_keys(arrival)
    dep_date_input = flights_form.find_element_by_id("departureDateRoundtrip0")
    dep_date_input.click()
    sleep(1)
    click_date_on_calendar(flights_form.find_element_by_xpath("//*[@id='ui-datepicker-div']"),
                           dep_date
                           )

    return_date_input = flights_form.find_element_by_id("departureDateRoundtrip1")
    return_date_input.click()
    click_date_on_calendar(flights_form.find_element_by_xpath("//*[@id='ui-datepicker-div']"),
                           dep_date + relativedelta(months=+3)
                           )
def click_filter(filters_div, filter_grp_id, filter_id):    
    filter_container = filters_div.find_element_by_xpath("./div/div[@data-dropdown-content-id='%s']" % filter_grp_id)
    filter = filters_div.find_element_by_id(filter_id)
    if not filter_container.is_displayed():
        filters_div.find_element_by_xpath("./div/a[@data-content-id='%s']" % filter_grp_id).click()
    filter.click()
    

def main():
    """
    Main program for realization of esky.pl task 
    with guidelines from eskypl_guidelines_in_polish.txt.
    """
    # 1.       Otworzenie strony
    main_url = "http://www.esky.pl/"
    esky_wd = webdriver.Firefox()
    print "Task #1: opening website: %s" % main_url
    esky_wd.get(main_url)
    # 2.       Pobranie i wyświetlenie w konsoli wartości ciastka esky_TCSI
    cookie_name = "esky_TCSI"
    print "Task #2: display value of cookie %s: %s" % (
        cookie_name, esky_wd.get_cookie(cookie_name)["value"]
    )
    # 3.       Wypełnienie danych formularza wyszukiwania 
    #(parametryzowane destynacje oraz daty wylotu/powrotu wyliczane zawsze 3mce do przodu)
    flights_form = esky_wd.find_element_by_css_selector("form.flights-qsf")
    print "Task #3: fill up flights form from %s" % main_url
    fill_flights_form(flights_form, 
                      departure="Hamburg", 
                      arrival="Katowice", 
                      dep_date=date.today()+relativedelta(days=+10)
                      )
    flights_form.submit()
    # 4.       Wykonanie prostego filtrowania na wynikach wyszukiwania (dowolna kombinacja)
    wait = WebDriverWait(esky_wd, 10)
    filters_div = wait.until(
        expected_conditions.visibility_of_element_located((By.ID, "filters"))    
    )
    filters_div.find_element_by_xpath("./div/span[@class='filters-text']").click() #show filters
    print "Show filters"
    click_filter(filters_div,
                 filter_grp_id = 'filterConnections', 
                 filter_id = "filterConnections_opt_1")
    click_filter(filters_div,
                 filter_grp_id = 'filterDepartureTime0', 
                 filter_id = "filterDepartureTime1_opt_12_18")    
    click_filter(filters_div,
                 filter_grp_id = 'filterDepartureTime0', 
                 filter_id = "filterDepartureTime0_opt_12_18") 
    click_filter(filters_div,
                 filter_grp_id = 'filterDepartureTime0', 
                 filter_id = "filterDepartureTime0_opt_12_18") 
    print "Task #4: using filters on results website"
    sleep(3)
    
    # 5.       Pobieranie kilku istotnych elementów pojedynczego lotu

    # 6.       Przejście na kolejny ekran płatności i wypełnienie formularza dowolnymi wartościami 
    # spełniającymi reguły walidacji

    # 7.       Wykonanie kilku asercji, biorąc pod uwagę dane uzyskane na formularzu wyszukiwania, 
    # wynikach i ekranie płatności.
    
    esky_wd.close()

if __name__ == "__main__":
    print "START"
    main()
    print "STOP"