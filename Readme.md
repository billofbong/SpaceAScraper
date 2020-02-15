# SpaceAScraper

Every US military member is familiar with Air Mobility Command's passenger terminal Facebook pages and the inconvenience they cause. Here's an example of a Space-A schedule:
![Space-A Schedule](https://wright.lv/i/i/Travis1.jpg)
Not particularly beautiful or info-filled...

This is a tool to scrape the AMC passenger terminals' Facebook pages, download the schedules, run OCR on them and plot the Space-A routes on a map (map currently in progress).
Hopefully this can eventually evolve into a hosted service that all US Military members can use.

## Getting started

Want to run this on your machine? Here's what you'll need:

### Prerequisites

* [Selenium](https://selenium-python.readthedocs.io/) - Headless browser for downloading the images
* [pytesseract](https://pypi.org/project/pytesseract/) - OCR framework built around Google's tesseract
	* [Pillow](https://pillow.readthedocs.io/en/stable/) - A requirement of pytesseract, also used for image manipulation

### Installation

* Install the prerequisites with pip
* Run SpaceAScraper.py from a CLI

### CLI Arguments

For a first time and each daily run, use the -s command to scrape the images
```
python3 SpaceAScraper.py -s
```

To read existing images, use the -r command
```
python3 SpaceAScraper.py -r
```

## Acknowledgments

* Thanks to [AMC](https://www.amc.af.mil/), whose terrible powerpoint screenshots inspired me to make this