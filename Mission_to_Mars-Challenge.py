
# Import Splinter and BeautifulSoup
import requests as re
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[3]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# ##  Visit the NASA Mars News site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://jpl.nasa.gov{img_url_rel}'
img_url

# To scrape entire table instead of scrapping each data in the rows and columns use pandas
df = pd.read_html('http://space-facts.com/mars/')[0] # This means pull only the first table or item in the list it encounters
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

# To turn the image back to html
df.to_html()


# # Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
# print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 
# ### Hemisphere
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
# Parse the data
html = browser.html
bs = soup(html, 'html.parser')


button = browser.find_by_id("product-section")

bs = soup(browser.html)

result = bs.find("div", class_="collapsible results")

# In[25]:


result.find_all("a")



# Find and click the full image button
href = []
for x in result.find_all("a"):
    image = x.get("href")
    href.append(image)


# In[27]:


list(set(href))

base_url = "https://astrogeology.usgs.gov"
images = [base_url + x for x in set(href)]
print(images)


# In[29]:


browser.visit(images[0])
html = browser.html 
BS = soup(html, "html.parser")
# print(BS.prettify())


# In[30]:


BS.find("ul")


# In[31]:


img_to_use= BS.find("ul").find("li").find("a").get("href")
img_to_use


# In[32]:


img_to_get =[]
for img in images:
    browser.visit(img)
    html = browser.html 
    BS = soup(html, "html.parser")
    img_to_use= BS.find("ul").find("li").find("a").get("href")
    img_to_get.append(img_to_use)

img_to_get

hrefs = list(set(href))

title = [" ".join(h.split('/')[-1].split('_')).title() for h in hrefs]

# # 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# # 3. Write code to retrieve the image urls and titles for each hemisphere.

for i in range(0,4):
    hemisphere = {}
    hemisphere["url"] = img_to_get[i]
    hemisphere["title"] = title[i]
    hemisphere_image_urls.append(hemisphere)
    
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# To quit the automated browser
browser.quit()

