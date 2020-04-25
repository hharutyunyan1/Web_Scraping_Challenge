def mars_scrape():
    #Dependencies
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    from bs4 import BeautifulSoup as bs
    import pandas as pd 
    import requests
    import pymongo
    import time 

    #Step1-Scraping

    #NASA Mars News

    #List full path to chromedrive, make sure to use r.
    url = "https://mars.nasa.gov/news/"

    driver = webdriver.Chrome(executable_path=r"C:/Users/hakha/OneDrive/Desktop/USC DataAnalyticsMain/USC DataAnalytics/11-Web-Scraping-and-Document-Databases/Homework/Scrape/chromedriver/chromedriver.exe")
    driver.get(url)

    request = requests.get(url)

    data = request.content

    soup = bs(data, 'html.parser')
    print(soup.prettify())

    news_title = soup.find_all('div', class_ = 'content_title')
    print(news_title)

    news_title = soup.find('div', class_= "content_title").find('a').text.strip()
    print(news_title)

    news_p = soup.find_all('div', class_= 'rollover_description_inner')
    news_p[1].text

    first_article_title = news_title
    first_article_paragraph = news_p[1].text

    #JPL Mars Space Images - Featured Image

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    driver.get(image_url)

    request_image = requests.get(image_url)

    image_data = request_image.content

    image_soup = bs(image_data, 'html.parser')
    print(image_soup.prettify())

    jpl_url = "https://www.jpl.nasa.gov/"
    image = image_soup.find('article')
    image_extension  = image['style'].split("('", 1)[1].split("')")[0]
    image_extension

    featured_image_url = jpl_url + image_extension

    #Mars Weather
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    driver.get(mars_weather_url)

    weather_request = requests.get(mars_weather_url)

    mars_weather_data = weather_request.content

    weather_soup = bs(mars_weather_data, 'html.parser')
    print(weather_soup.prettify())

    mars_weather = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    print(mars_weather.text)

    mars_weather_tweet = mars_weather.text

    #Mars Facts
    mars_facts_url = "https://space-facts.com/mars/"
    driver.get(mars_facts_url)

    mars_fact_tables = pd.read_html(mars_facts_url)
    print(mars_fact_tables)

    mars_facts_df = mars_fact_tables[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df

    mars_facts_table_html = mars_facts_df.to_html()

    mars_facts_table_html.replace('\n', '')
    print(mars_facts_table_html)

    html_text_file = open("mars_facts_table.html", "w")
    html_text_file.write(mars_facts_table_html)
    html_text_file.close()

    #Mars Hemispheres
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(mars_hemisphere_url)
    mars_hemisphere_response = requests.get(mars_hemisphere_url)

    if mars_hemisphere_response.status_code == 200:
        mars_hemisphere_html = mars_hemisphere_response.text

    def get_full_image_link(link):

        response = requests.get(link)

        if response.status_code == 200:
            html = response.text
        
        soup = bs(html, "html.parser")
        
        img_link = soup.find("a", text="Original").get("href")
        title = soup.find("h2", class_="title").text.split(" Enhanced")[0]
            
        return [title, img_link]

    mars_hemisphere_soup = bs(mars_hemisphere_html, "html.parser")
    link_elements = mars_hemisphere_soup.findAll("a", {"class": "itemLink product-item"})
    full_page_links = [dict(title=get_full_image_link("https://astrogeology.usgs.gov" + le.get('href'))[0], img_url=get_full_image_link("https://astrogeology.usgs.gov" + le.get('href'))[1]) for le in link_elements]

    return dict(first_article_title = first_article_title, 
                first_article_paragraph = first_article_paragraph,
                featured_image_url = featured_image_url,
                mars_weather_tweet = mars_weather_tweet,
                mars_facts_df = mars_facts_df.to_dict('records'),
                full_page_links = full_page_links
    )

if __name__ == "__main__":

    print(mars_scrape())