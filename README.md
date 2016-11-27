# Junction 2016 Project on Hatespeech
(Hacktathon Helsinki - 25-27 nov. 2016)

[https://devpost.com/software/hackhate](https://devpost.com/software/hackhate)


### Inspiration
The last elections have shown that politicians are getting away with posting hate speech and false information on their social media feeds.

### What it does
We want to provide a tool that allows to analyse politicians social media feeds in regard to hate, information credibility and sentiment analysis. Moreover, it's not only a search page, but also a chrome plugin to directly extract and check content from websites.

### How we built it
We have used several tools:

- main language is python, pandas and nltk for sentiment analysis
- the application is served with django
- hatebase database for detecting hate speeches and words
- our own database and duck duck go search for checking content credibility
- javascript for interactive content on the webpage and for the chrome extension
- twitter, facebook and reddit api for retrieving content
- wikidata and sparql for fetching information about politicians

### Challenges we ran into
- Facts checking is tremendously hard
- website credibility
- hate speech analysis is not just single words checking
- wikidata querying is not easy and can take a while
- parsing and scrapping websites and search engines results
- Not enough time to work on our own classifier, even though we have annotated data

### Accomplishments that we're proud of
- Good looking web application that works
- the chrome extension is simple but effective
- working hate speech detection

### What we learned
- generating and using apis
- using and combining multiple content sources
- generating meaningful visualizations
- building chrome extension

### What's next for HackHate
- Getting a large dataset from reddit data and training our own machine learning classifier
- Extending our database for credibility checking
- annotating the web pages with chrome extension to give live credibility checking

Built With
python, django, twitter, facebook-graph, machine-learning, nltk, sparql, wikidata, chrome

### Try it out
[http://hackhate.huguesverlin.fr](http://hackhate.huguesverlin.fr)
