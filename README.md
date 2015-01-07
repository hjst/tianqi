# Tiānqì (天气)

This is a little python program I wrote to fetch current weather and air quality
summaries from the [China Meteorological Administration][CMA] (CMA) website, and the
[AQICN][] site.

It's designed for use on the command line, and outputs a quick summary for your
city. It's useful to check quickly in the morning if you need an umbrella or to
be aware of air pollution for the day.

All the existent command line weather programs I found use NOAA data, or METAR
or similar. This data is often not particularly accurate for China's cities, and
doesn't include air quality readings. So, if you're living in China and want
a quick weather summary for your terminal, you may find this useful.

## Usage

```
$ tianqi shanghai
High: 19ºC :: Light Rain :: AQI 116 :: Umbrellas ☂

$ tianqi beijing
High: 6ºC :: Cloudy :: AQI 211 ☹  :: No umbrellas

$ tianqi --help
Tiānqì (天气) - Weather & AQI summary for Chinese cities

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
```

## How it works

Sadly, neither the CMA nor AQICN sites offer any APIs so I resorted to using
[BeautifulSoup][] to simply scrape their pages. Specifically, the data scraped
is as follows:

* "Headline" Air Quality Index measurement, which is PM2.5
* AM/PM forecast summary for current morning or afternoon
  - Description, e.g. "Cloudy" or "Light Rain"
  - Predicted highest temperature
* The CMA "Umbrella Index", which is handy to check in the morning

## Requirements

* Python ≥ 3.2.2 (older versions only have strict [html.parser][], no good for
  government websites)
* [BeautifulSoup][] 4 (`pip install beautifulsoup4`)
* [docopt][] ≥ 1.6.2 (`pip install docopt`)

Everything is done in python, with no assumptions made about shells or
filesystems etc. so this should work fine on Mac, Windows, anywhere you can run
python.

## Installation

I haven't packaged this properly yet, so for the moment you'll need to clone
this repo somewhere, install the dependencies (see above) and link the script
into your path. I just do this:

    $ ln -s ~/git/tianqi/tianqi.py ~/bin/tianqi

## Why?

The CMA tends to have the more accurate weather data (in my experience) and
their "umbrella index" is useful, but their AQI readings are pretty consistently
lower than AQICN (which averages multiple measuring stations and offers US
embassy/consulate data). Conversely AQICN has more reliable AQI data, but gets
its weather data from Yahoo, which isn't as accurate as the CMA.

Also, I just wanted to type one command in the morning and immediately see only
the data I care about.

## Alternatives

If you're not in China this is useless, but if you'd like something similar,
take a look at:

* [Weatherme][] (node.js) uses data from forecast.io, which is great if you're
  in the USA or UK
* [ansiweather][] (bash) uses the OpenWeatherMap API, also uses ANSI colours &
  unicode symbols
* [Weather][] (python) uses NOAA data and it's packaged for various linux
  distros

## TODO

* Add more error handling for timeouts, missing data etc.
* Use new asyncio bits in 3.3 to run HTTP requests concurrently
* Split up `scrape_conditions_at()` function, it's a mess
* Add colour-coding for AQI data, red for >150 maybe?
* Add verbose output option with more forecast data
* Add more city shortcuts
* Package it properly for PyPI?

## Licence 

ISC licensed, go wild. See the bundled [LICENSE][] file for more details.

[CMA]: http://www.cma.gov.cn/
[AQICN]: http://aqicn.org/
[html.parser]: https://docs.python.org/3/library/html.parser.html
[BeautifulSoup]: http://www.crummy.com/software/BeautifulSoup/
[docopt]: https://github.com/docopt/docopt
[Weatherme]: https://github.com/shapeshed/weatherme
[ansiweather]: https://github.com/fcambus/ansiweather
[Weather]: http://fungi.yuggoth.org/weather/
[LICENSE]: https://github.com/hjst/tianqi/blob/master/LICENSE
