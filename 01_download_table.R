library(rvest)
library(dplyr)


url <- "https://www.strava.com/running_races/2428/results?page="
url_i <- paste0(url, "1")

page <- read_html(url_i)
table <- html_table(page, fill = TRUE)
table_1 <- table[[1]]
