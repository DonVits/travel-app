# **Tourist Destination Recommendations Based on Data**
### **Programming for Data Science**

## Author(s)
- Don Vito Dapat
- Ibtissem Gamaoun
- Kseniya Mazur


## Project characteristics 

As a tourist, I would like to see some recommendations on which country I should visit next. These recommendations will be based on different criteria such as: Visa requirements, average prices of hotels/accommodations, average flight ticket price coming from country of origin, and number of tourists who visited the country from different countries including: EU(Schengen), USA, Japan, Singapore, Australia, and Canada.  



## Used data sources
Airbnb data from major cities: http://insideairbnb.com/get-the-data/
Passport index: https://github.com/ilyankou/passport-index-dataset
Flight prices data scraped from: https://www.kayak.com/
Tourist Data for each EU country: https://ec.europa.eu/eurostat/databrowser/view/tour_dem_ttw/default/table?lang=en

## Used packages
- Anvil - A framework used for developing web applications with Python
- Pandas - Library used for data analytics and manipulation
- Numpy - for scientific computing with Python.
- Matplotlib - comprehensive library for creating static, animated, and interactive visualizations in Python.
- BeautifulSoup - Package for parsing HTML
- Selenium Webdriver - Used for automated web browsing for scraping data

## The general elements of a program (pseudo-code)

- User interacts with a front-end interface built on Anvil
- Front-end will interact with a service layer which performs the data analysis
- Users can select whether to get recommendations for a travel destination or just explore a destination.
- Datasets on Visa will be loaded using pandas and visualized using the world map
- Flight and accommodation prices will be loaded based on the selected country and visualized using a histogram



## Main problems that occurred during the implementation
- No available dataset on flight prices can be obtained online so a web scraper was built using Selenium and BeautifulSoup
- Due to large amounts of data, only countries of interest will be chosen





