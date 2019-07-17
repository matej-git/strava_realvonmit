library(rvest)
library(dplyr)
library(tidyr)

url <- paste0('https://www.strava.com/running_races/', url, '/results?page=')

i <- 1
url_i <- paste0(url, i)
page <- read_html(url_i)
table <- html_table(page, fill = TRUE)[[1]]
links <- page %>% 
  html_nodes('.dense.striped') %>% 
  html_nodes('a') %>% 
  html_attr('href')

athlet_url <- links[seq(1,length(links),3)]
race_url <- links[seq(3,length(links),3)]

table['athlet_url'] <- athlet_url
table['race_url'] <- race_url

table_final <- table 

statment <- T

while (statment)
{
  i <- i + 1
  url_i <- paste0(url, i)
  page <- read_html(url_i)
  table <- html_table(page, fill = TRUE)[[1]]
  
  statment <- dim(table)[1] != 0
  
  if (statment) {
    links <- page %>%
      html_nodes('.dense.striped') %>%
      html_nodes('a') %>%
      html_attr('href')
    
    athlet_url <- links[seq(1, length(links), 3)]
    race_url <- links[seq(3, length(links), 3)]
    
    table['athlet_url'] <- athlet_url
    table['race_url'] <- race_url
    
    table_final <- union(table_final, table)
  }
}

write.csv(table_final, paste0("data/raw/",city,"_",type,"_",year,"_raw",".csv"))

