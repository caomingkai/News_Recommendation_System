# News Recommendation System

## About
A internet-based news aggregator, providing hot news from popular news sources, with recommendation feature based on users' preference.

## Tech stack:
- Front end:( React, Node.js, JWT)
    + Built a responsive single-page web application for users to browse news (React, Node.js, RPC, SOA, JWT)

- Back end:(Python RPC, MongoDB, Redis, RabbitMQ, TF-IDF, NLP, )
    + Service Oriented, multiple backends serving via JSON RPC
    + Implemented a data pipeline which monitors, scrapes and deduplicates news

- Machine Learning back end: (Tensorflow, DNN, NLP)
    + Designed and built an offline training pipeline for news topic modeling
    + Implemented a click event log processor which collects users' click logs, updated a news model for each user
    + Deployed an online classifying service for news topic modeling using trained model
