# News Recommendation System

## About
An internet-based news aggregator, providing hot news scraping on popular news sources, with recommendation feature based on users' preference with the help of Machine Learning.

## Tech stack:
- __Front end__:( React, Node.js, JWT)
    + Built a responsive single-page web application for users to browse news (React, Node.js, RPC, SOA, JWT)

- __Back end__:(Python RPC, MongoDB, Redis, RabbitMQ, TF-IDF, NLP, )
    + Service Oriented, multiple backends serving via JSON RPC
    + Implemented a data pipeline which monitors, scrapes and deduplicates news

- __Machine Learning back end__: (Tensorflow, DNN, NLP)
    + Designed and built an offline training pipeline for news topic modeling
    + Implemented a click event log processor which collects users' click logs, updated a news model for each user
    + Deployed an online classifying service for news topic modeling using trained model
