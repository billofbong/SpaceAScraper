from selenium import webdriver
import time
import os
import csv
import urllib.request as req
import sys
import pytesseract
from PIL import Image, ImageOps


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
        time.sleep(0.5)
        images = []
        for i in driver.find_elements_by_tag_name('img'):
            if i.rect.get('height') == 200 and i.rect.get('width') == 200:  # get the photo elements in the album
                images.append(i)
        j = 0
        for i in images:
            i.click()
            time.sleep(0.5)
            print("Saving " + os.path.join(os.path.curdir, os.path.join('Images', base['BaseName']) + str(j) + '.png'))
            req.urlretrieve(driver.find_element_by_class_name('spotlight').get_attribute('src'),
                            os.path.join(os.curdir, 'Images', base['BaseName'] + str(j) + '.png'))
            driver.find_element_by_class_name('_xlt').click()  # click the X
            j += 1
    print("****************")
    print("Done scraping...")
    print("****************")
    driver.close()


if '-s' in str(sys.argv):  # run with -s argument to scrape
    with open('bases.csv') as file:
        reader = csv.DictReader(file)
        get_images_csv(list(reader))

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

no_invert = ["SeaTac", "McChord", "Norfolk", "Travis"]  # These have black text already, do not invert

if not '-r' in str(sys.argv):  # save text files only / read-only
    print("****************")
    print("Beginning OCR...")
    print("****************")
    for filename in os.listdir("Images"):
        if not filename.startswith("tr_") and filename.endswith(".png"):
            im = Image.open(os.path.join('Images', filename))
            if filename[0:-5] not in no_invert:
                im = ImageOps.invert(im)  # only invert if the base is not in no_invert
            filename = "tr_" + filename
            dep = pytesseract.image_to_string(im, config='--psm 6').upper()
            if "DEPARTURE" in dep:
                print("Saving " + (os.path.join('Images', filename)))
                im.save(os.path.join('Images', filename))

print("*********************")
print("Saving OCR Results...")
print("*********************")
make_folder("Results")

# The reason for using two different loops here is so I can use different psm settings for debugging
# TODO: Integrate loops
for filename in os.listdir("Images"):
    if filename.startswith("tr_") and filename.endswith(".png"):
        content = pytesseract.image_to_string(os.path.join('Images', filename), config='--psm 3')
        print("Saving " + os.path.join('Results', filename[3:-4] + ".txt"))
        with open(os.path.join('Results', filename[3:-4] + ".txt"), 'w') as f:
            f.write(content)
