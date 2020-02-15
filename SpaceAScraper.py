from selenium import webdriver
import time
import os
import csv
import urllib.request as req
import sys


def make_folder(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Folder " + path + " already exists")
    else:
        print("Created folder " + path)


def get_images_csv(csv_dict):
    make_folder("Images")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # make headless chrome
    options.add_argument("window-size=3000,3000")  # make the window large so no scrolling required
    driver = webdriver.Chrome(options=options)
    for base in csv_dict:
        print("Scraping " + base['BaseName'] + "...")
        driver.get(base["URL"])
        time.sleep(0.25)
        images = []
        for i in driver.find_elements_by_tag_name('img'):
            if i.rect.get('height') == 200 and i.rect.get('width') == 200:  # get the photo elements in the album
                images.append(i)
        j = 0
        for i in images:
            i.click()
            time.sleep(0.5)
            print(os.path.join(os.path.curdir, os.path.join('Images', base['BaseName']) + str(j) + '.png'))
            req.urlretrieve(driver.find_element_by_class_name('spotlight').get_attribute('src'),
                            os.path.join(os.curdir, 'Images', base['BaseName'] + str(j) + '.png'))
            driver.find_element_by_class_name('_xlt').click()  # click the X
            j += 1
    driver.close()


if '-r' in str(sys.argv):  # run with -r argument to refresh scrape
    with open('bases.csv') as file:
        reader = csv.DictReader(file)
        get_images_csv(list(reader))

