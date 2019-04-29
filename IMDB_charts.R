library(RMySQL)
library(dbConnect)
library(ggplot2)
con <- dbConnect(RMySQL::MySQL(),
                 dbname = "looqbox_challenge", 
                 host="35.199.127.241", 
                 port = 3306, 
                 user="looqbox-challenge", 
                 password = "looq-challenge")

dbListTables(con)

tfd <- dbGetQuery(con, paste("select * from IMDB_movies"))

summary(tfd)

tfd_drama <- dbGetQuery(con, paste("select * from IMDB_movies where genre = 'Drama'"))

tfd_comedy <- dbGetQuery(con, paste("select * from IMDB_movies where genre = 'Comedy'"))


#Histogram for Votes x Rating
qplot(tfd$Rating, geom = "histogram",
      main = "Most Rated Movies", 
      xlab = "Rate",
      ylab = "Votes",
      fill=I("lightblue"), 
      col=I("black"),
      binwidth = 0.5,
)

#Metascore x Votes
ggplot(tfd, aes(x=Votes, y=Metascore)) + geom_point(color="green")

#Comparing rating of Drama Movies
ggplot(tfd_drama, aes(x=Title, y=Rating)) + 
      geom_bar(stat='identity', aes(fill= Rating), width=0.5) +
      labs(subtitle="Scale Rating of Drama Movies", 
      title= "Drama Movies") + 
      coord_flip()

#Comparing rating of Comedy Movies
ggplot(tfd_comedy, aes(x=Title, y=Rating)) + 
  geom_bar(stat="identity", width=.5, fill="tomato3") + 
  labs(title="Comedy Movies", 
       subtitle="Scale Rating of Comedy Movies") + 
  theme(axis.text.x = element_text(angle=65, vjust=0.6))
