from flask import Flask, request, render_template, jsonify
from utils import *
import scrape_bwin as bwin_scraper
import scrape_betfair as betfair_scraper


app = Flask(__name__)

@app.route("/api/scrape_bwin", methods=["GET"])
def api_scrape_bwin():
    driver = bwin_scraper.start_browser('https://sports.bwin.com/en/sports/live/football-4?fallback=false')
    bwin_scraper.close_popup(driver)
    bwin_scraper.accept_cookies(driver)
    bwin_scraper.choose_value_from_dropdown(driver)
    btts, teams = bwin_scraper.scrape_odds(driver)
    dict_gambling = bwin_scraper.store_odds(teams, btts)
    return jsonify(dict_gambling)

@app.route("/api/scrape_betfair", methods=["GET"])
def api_scrape_betfair():
    driver = betfair_scraper.start_browser('https://www.betfair.com/sport/inplay')
    betfair_scraper.accept_cookies(driver)
    betfair_scraper.choose_value_from_dropdown(driver)
    btts, teams = betfair_scraper.scrape_odds(driver)
    dict_gambling = betfair_scraper.store_odds(teams, btts)
    return jsonify(dict_gambling)

@app.route("/api/calc_surebets", methods=["GET"])
def api_index():
    df_bwin, df_betfair = read_dataframes('df_bwin', 'df_betfair')
    df_surebet_bwin_betfair = clean_and_combine_dataframes(df_bwin, df_betfair)
    surebet = find_surebet(df_surebet_bwin_betfair)
    surebets = calculate_surebets(surebet, 150)
    return jsonify(surebets)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)