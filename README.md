# v_crawler

v_crawler is a simple project to crawl the Amazon Prime Video platform for movies and series.

It is using the [Scrapy Framework](https://github.com/scrapy/scrapy) and extracts various information about the found content and saves them to a AWS DynamoDB table.

## Requirements

### Privoxy

1. Install Privoxy
2. Uncomment the following line in the **config.txt**:
     
    ```forward-socks4a   /               127.0.0.1:9050 .```

3. Change the given port from _9050_ to _9150_

### TOR

1. Install the TOR browser and have it running
2. If you want to make use of the TOR service you have to skip step 2 of Privoxy and change the ports inside the code to 9050.

### PostgreSQL

1. Create a "database.ini" file with the following schema:

    ```ini
    [postgresql]
    host=<yourHost>
    port=<yourPort>
    dbname=<yourDbName>
    user=<yourUser>
    password=<yourPassword>
    ```
    
2. Create a table using the following specs:

    ```SQL
    CREATE TABLE amazon_video_de
    (
        movie_id VARCHAR(10) not null primary key,
        url VARCHAR(255) not null,
        title VARCHAR(255) not null,
        rating FLOAT,
        imdb FLOAT,
        genres VARCHAR[],
        year NUMERIC,
        fsk NUMERIC,
        movie_type varchar(255),
        poster BYTEA
    )
    ```
    
    - To improve the query speed you want to create an index for the LOWER() funtion of PostgreSQL:
    ```SQL
    CREATE INDEX ON amazon_video_de (LOWER(title))
    ```
    
    
### IMDb API server

1. Install my [imdb-api-server](https://github.com/BreakBB/imdb-api-server)
2. By default this runs on localhost:8555
    
    
### Python dependencies

1. Install the python dependencies using the **requirements.txt**
 
