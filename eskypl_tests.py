#-*- coding: utf-8 -*-
#!/usr/bin/env python
"""
This is a simple script for tests esky.pl website functionality 
by Selenium/Webdriver Python module.
"""
from selenium import webdriver

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

    # 4.       Wykonanie prostego filtrowania na wynikach wyszukiwania (dowolna kombinacja)

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