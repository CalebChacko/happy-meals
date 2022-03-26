from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def setup_browser(debug, download_path):
    opts = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_path}
    opts.add_experimental_option("prefs", prefs)
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])

    if not debug:
        opts.add_argument("--headless")

    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts)
    print('Chrome Driver Created')
    return browser