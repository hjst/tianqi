#!/usr/bin/env python3
"""Tiānqì (天气) - Weather & AQI summary for Chinese cities

Usage:
    tianqi <city>
    tianqi <city> --aqicn-id=<aqicn-id>
    tianqi <city> --cma-id=<cma-id>
    tianqi --list-cities
    tianqi --aqicn-id=<aqicn-id> --cma-id=<cma-id>
    tianqi (-h | --help)

Options:
    -h --help         Show this screen
    -l --list-cities  Show the internal list of predefined city names
    --aqicn-id=<id>   AQICN location id, e.g. guangdong/fushan/wanliang
    --cma-id=<id>     CMA location id, e.g. 101280800 (Foshan)

"""

import sys
import json
import urllib.request
from docopt import docopt
from bs4 import BeautifulSoup

predefined_locations = json.load(open(sys.path[0]+'/locations.json'))

def main(args):
    #print(args)
    if args['<city>']:
        loc = get_location(args['<city>'], predefined_locations,
                args['--aqicn-id'], args['--cma-id'])
        tianqi = scrape_conditions_at(loc)
        render_conditions(tianqi)
    elif args['--list-cities']:
        render_locations_list(predefined_locations)
    else:
        # no city specified, use manual location id overrides
        tianqi = scrape_conditions_at({'cma_id': args['--cma-id'],
            'aqicn_id': args['--aqicn-id']})
        render_conditions(tianqi)

def scrape_conditions_at(location={}):
    # China Meteorological Administration HTTP request
    cma_url = 'http://en.weather.com.cn/weather/%s.shtml'\
        '?index=3' % location['cma_id']
    cma_response = urllib.request.urlopen(cma_url)
    cma_page = BeautifulSoup(cma_response.read())

    # AQICN HTTP request
    aqicn_url = 'http://aqicn.org/city/%s/m' % location['aqicn_id']
    aqicn_request = urllib.request.Request(aqicn_url)
    # if you don't supply a 'real' user-agent header AQICN returns
    # different data, I have no idea why
    aqicn_request.add_header('User-agent', 'Mozilla/5.0 (iPad; '\
        'CPU OS 8_0 like Mac OS X) AppleWebKit/538.34.9 '\
        '(KHTML, like Gecko) Mobile/12A4265u')
    aqicn_response = urllib.request.urlopen(aqicn_request)
    aqicn_page = BeautifulSoup(aqicn_response.read())

    # Populate the conditions dict by scraping the pages
    # Note here that I'm using .find() instead of .find_all because
    # in each case the result I want is very specifically the first
    # one - the markup on the CMA pages in particular is horrible,
    # with no ids on key elements, and a real div/class mess.
    conditions = {}
    conditions['aqi'] = aqicn_page.find("div", class_="aqi").string
    
    umbrella_div = cma_page.find("h2", text="Umbrella Index").parent
    conditions['umbrella'] = umbrella_div.find("i").string
    forecast = cma_page.find("div", class_="day7")
    today = forecast.find_all("div", class_="fl")
    # The 7day forecast pager thing is split by day/night, but instead
    # of moving everything along to show a 24h window from *now*, they
    # just blank out the first div.fl - so if those variables now contain
    # None we need to use the fourth div.fl. This is so dumb.
    if today[0].find("p").string:
        # the first div contains data, i.e. use the morning forecast
        conditions['weather'] = today[0].find("p").string
        conditions['temp_c'] = today[0].find("i", class_="wC").string
        conditions['temp_f'] = today[0].find("i", class_="wF").string
    else:
        # the first div contains empty elements, i.e. use the evening
        # forecast instead
        conditions['weather'] = today[3].find("p").string
        conditions['temp_c'] = today[3].find("i", class_="wC").string
        conditions['temp_f'] = today[3].find("i", class_="wF").string
    return conditions

def render_conditions(c={}):
    if int(c['aqi']) > 200:
        c['aqi_icon'] = ' ☹'
    elif int(c['aqi']) < 50:
        c['aqi_icon'] = ' ☺️'
    else:
        c['aqi_icon'] = ''

    print("High: {}ºC :: {} :: AQI {}{} :: {} ☂".format(
        c['temp_c'], c['weather'], c['aqi'], c['aqi_icon'], c['umbrella']))

def render_locations_list(locations):
    for key in sorted(locations):
        print(key)

def get_location(city, predefined, aqi_override=None, cma_override=None):
    # normalise case for matching
    try: city = city.lower()
    except AttributeError:
        # objects that don't implement .lower() are fine, just match as-is
        pass

    # if the city name is unknown, do a quick'n'dirty error message & halt
    try: predefined[city]
    except KeyError:
        print("Unknown city")

    location = predefined[city]
    # use any supplied overrides
    if aqi_override: location['aqicn_id'] = aqi_override
    if cma_override: location['cma_id'] = cma_override

    return location

if __name__ == '__main__':
    main(docopt(__doc__))

