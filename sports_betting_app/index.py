from flask import Flask, request, render_template, jsonify
from utils import *
import scrape_bwin as bwin_scraper
import scrape_betfair as betfair_scraper


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/scrape_bwin", methods=["GET"])
def scrape_bwin():
    driver = bwin_scraper.start_browser('https://sports.bwin.com/en/sports/live/football-4?fallback=false')
    bwin_scraper.close_popup(driver)
    bwin_scraper.accept_cookies(driver)
    bwin_scraper.choose_value_from_dropdown(driver)
    btts, teams = bwin_scraper.scrape_odds(driver)
    bwin_odds = bwin_scraper.store_odds(teams, btts)
    return render_template("scrape.html", odds=bwin_odds, website='Bwin')

@app.route("/scrape_betfair", methods=["GET"])
def scrape_betfair():
    driver = betfair_scraper.start_browser('https://www.betfair.com/sport/inplay')
    betfair_scraper.accept_cookies(driver)
    betfair_scraper.choose_value_from_dropdown(driver)
    btts, teams = betfair_scraper.scrape_odds(driver)
    betfair_odds = betfair_scraper.store_odds(teams, btts)
    return render_template("scrape.html", odds=betfair_odds, website='Betfair')

@app.route("/calc_surebets", methods=["GET"])
def calc_surebets():
    df_bwin, df_betfair = read_dataframes('df_bwin', 'df_betfair')
    df_surebet_bwin_betfair = clean_and_combine_dataframes(df_bwin, df_betfair)
    surebet = find_surebet(df_surebet_bwin_betfair)
    surebets = calculate_surebets(surebet, 150)
    return render_template("index.html", surebets=surebets)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)