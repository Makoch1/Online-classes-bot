import os
import stat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

st = os.stat('chromedriver')
os.chmod('chromedriver', st.st_mode | stat.S_IEXEC)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-dev-shm-usage')
DRIVER = webdriver.Chrome('./chromedriver', options=chrome_options)
WOTD_LINK = 'https://www.merriam-webster.com/word-of-the-day'

def get_wotd():
    # returns: dict
    data = {
        'word':'',
        'definition': '',
        'example': ''
    }

    DRIVER.get(WOTD_LINK)
    data['word'] = DRIVER.find_element_by_tag_name('h1').text

    def_div_paragraphs = DRIVER.find_element_by_class_name('wod-definition-container').find_elements_by_tag_name('p')
    data['definition'] = def_div_paragraphs[0].text
    data['example'] = def_div_paragraphs[1].text
    return data