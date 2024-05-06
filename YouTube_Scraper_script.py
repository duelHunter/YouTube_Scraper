from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def scroll_page_slowly(driver):
    action = ActionChains(driver)
    for _ in range(10000):
        action.send_keys(Keys.ARROW_DOWN).perform()


###########################################################################
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

search_query = "AI video editing"


driver.get(f'https://www.youtube.com/results?search_query={search_query}')
scroll_page_slowly(driver)

wait = WebDriverWait(driver, 10)
contents_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "ytd-video-renderer")))

# element2 = driver.find_element(By.ID, "contents")
# element3 = driver.find_element(By.CSS_SELECTOR, "yt-formatted-string.style-scope")

##################################################################################################
#creating csv header title
header_titles = ["Channel name", "Video title", "Views", "Duration", "Channel link", "Watch link"]

# name of csv file
filename = "youtube_data.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(header_titles)


##################################################################

for i in driver.find_elements(By.TAG_NAME, "ytd-video-renderer") :
    try:
        channel_name = i.find_element(By.CSS_SELECTOR, "#channel-info .ytd-channel-name a").text
        title = i.find_element(By.TAG_NAME, "yt-formatted-string").text
        views = i.find_element(By.CSS_SELECTOR, "#metadata span").text
        duration = i.find_element(By.CSS_SELECTOR, "#time-status span").text
        channel_link = i.find_element(By.CSS_SELECTOR, "#channel-info .ytd-channel-name a").get_attribute('href')
        watch_link=i.find_element(By.CSS_SELECTOR,'#thumbnail').get_attribute('href')

        # thumb_4to = i.find_element(By.CLASS_NAME, "yt-core-image").get_attribute('src')


        data_list = [channel_name, title, views, duration, channel_link, watch_link]
        print(data_list)

        with open(filename, 'a', encoding = "utf-8", newline = '') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data_list)

    except Exception as e:
        print(e)
        break
