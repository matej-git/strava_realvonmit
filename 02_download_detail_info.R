library(rvest)
library(dplyr)
library(tidyr)

url <- 'https://www.strava.com/activities/2136186226'
url_login <- 'https://www.strava.com/login'
session <- html_session(url_login)

form <- html_form(read_html(url_login))[[1]]
filled_form <- set_values(form,
                          email = 'mkarkalik@gmail.com',
                          password = 'akosamas')

submit_form(session, filled_form)

page_login <- jump_to(session, url)
page <- read_html(page_login)

boots <- page %>%
  html_table()
  
  
  html_nodes('.gear-name') %>% 
  html_text()
