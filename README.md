# metal-music-search-engine

## Metal Music Search Engine
Welcome to the Metal Music Search Engine project! This is a web-based search engine specifically designed for metal music enthusiasts. Built using Flask, Elasticsearch, and Kibana, the project offers advanced search capabilities for exploring metal songs and related information.

## Features
One-word and Multi-word Search: Search for songs, artists, or albums using one or multiple keywords.
Partial Match: Supports partial matching, making it easier to find songs even if you don't know the full title or artist name.
Ranking: Results are ranked based on relevance, with song names and artist names given higher priority.
Dynamic Search Interface: The interface dynamically updates search results with features like pagination.
Elasticsearch Integration: Uses Elasticsearch for indexing and retrieving data efficiently.
Kibana Dashboard: Analyze search trends and explore song data through interactive visualizations in Kibana.
## Technologies Used
Flask: A lightweight web framework for Python used to create the web application.
Elasticsearch: A distributed search engine for storing and querying song data.
Kibana: A data visualization tool for exploring Elasticsearch data.
HTML/CSS/JavaScript: For building the front-end interface.
Python: Core language for server-side logic and data handling.


IR_WEBSITE/
├── static/  # Static files (CSS, images, JS)
│   ├── home.css
│   ├── script.js
│   └── photo/  # Images for banners and UI
├── templates/  # HTML templates
│   ├── home.html  # Home page
│   └── search.html  # Search results page
├── scripts/  # Python scripts
│   ├── clean_data.py  # Clean and process song data
│   ├── elasticsearch_loader.py  # Load data into Elasticsearch
│   ├── music_data_collector.py  # Collect song data from APIs
│   └── search_app.py  # Flask application for search engine
├── songs.json  # Original song data in JSON format
├── songs-bulk.ndjson  # NDJSON file for bulk loading into Elasticsearch
├── updated_songs.ndjson  # Cleaned and updated NDJSON file
└── README.md

Installation
Prerequisites
Python 3.7+
Elasticsearch 8.x
Kibana 8.x

Setup
Clone the repository:
Install required Python packages:
Start Elasticsearch and Kibana:
Ensure Elasticsearch is running on https://localhost:9200.
Kibana should be accessible on http://localhost:5601.

## Usage
1. Search for Metal Songs:
  Enter a song title, artist, or lyrics in the search bar.
  View search results ranked by relevance.
2. Analyze Data in Kibana:
  Use the Kibana dashboard to explore indexed data and visualize trends.

## Future Improvements
  Advanced Filters: Add filters for genre, release year, etc.
  User Authentication: Allow users to save favorite songs or search history.
  Enhanced Data Collection: Integrate more APIs for richer song data.
## Contributing
  Contributions are welcome! Please fork the repository and submit a pull request.
