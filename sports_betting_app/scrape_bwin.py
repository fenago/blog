from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import pickle
import re


def start_browser(url):
    options = Options()
    options.headless = True
    options.add_argument('window-size=1920x1080') 

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver

def close_popup(driver):
    try:
        cross_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ui-icon theme-ex')]")))
        cross_icon.click()
    except:
        pass

def accept_cookies(driver):
    try:
        accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-success']")))
        accept_cookies.click()
    except:
        pass

def choose_value_from_dropdown(driver):
    try:
        dropdown_1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-view"]/ms-live/ms-live-event-list/div/ms-grid/ms-grid-header/div/ms-group-selector[1]/ms-dropdown/div')))
        dropdown_1.click()
        dropdown_1.find_element_by_xpath('//*[@id="main-view"]/ms-live/ms-live-event-list/div/ms-grid/ms-grid-header/div/ms-group-selector[1]/ms-dropdown/div[2]/div[10]').click()
    except:
        pass

def scrape_odds(driver):
    btts, teams = [], []
    box = driver.find_element_by_xpath('//ms-grid[contains(@sortingtracking,"Live")]') 
    rows = WebDriverWait(box, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'grid-event')))

    for row in rows:
        odds = row.find_elements_by_class_name('grid-option-group')
        try:
            empty_events = row.find_elements_by_class_name('empty') #removing empty odds
            odd = odds[0] if odds[0] not in empty_events else ''
        except:
            pass
        if(odd):
            btts.append(odd.text)
            grandparent = odd.find_element_by_xpath('./..').find_element_by_xpath('./..')
            teams.append(grandparent.find_element_by_class_name('grid-event-name').text)

    driver.quit()
    return btts, teams

def store_odds(teams, btts):
    #unlimited columns
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    dict_gambling = {'Teams':teams,'btts': btts}

    df_bwin = pd.DataFrame.from_dict(dict_gambling)
    df_bwin = df_bwin.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    output = open('df_bwin', 'wb')
    pickle.dump(df_bwin, output)
    output.close()
    bwin_odds = []
    for team, odds in zip(dict_gambling['Teams'], dict_gambling['btts']):
        bwin_odds.append({
            'Team': team,
            'Odds': odds
        })
    return bwin_odds




