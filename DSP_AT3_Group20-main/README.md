# Database Explorer Web App

## DSP Group 20

Members:

- Name: Phuong Thao Nguyen - Student ID: 24594665
- Name: Tingwei He - Student ID: 14360440
- Name: Somayeh Amraee - Student ID: 14229064
- Name: Justin Mah - Student ID: 13290085

## Description

This is a containerised interactive web application in Python that helps data scientists to explore their datasets. They can connect to databases, view table contents, important descriptive statistics, etc. in order to understand their data and identify its limitation.

The project includes two services:

1. Streamlit application
2. Postgres database

This web application will connect to a Postgres database and perform some exploratory data analysis on selected tables. The web application is containerised with Docker and will be running Python 3.8.2.

These are features of this web application:

1. Debugging with Streamlit session state value
2. Menu for connecting to a database and selecting a table
3. Container with 5 tabs:

- Overall information of the selected table
- Exploration of the table content
- Information on each numeric column
- Information on each text column
- Information on each datetime column

## How to Setup

1. Install Docker application from www.docker.com
2. Install Git application (in case you clone the code from Github instead of using zip file)
3. In terminal, type the following command to download the project into your local machine:

```bash
git clone git@github.com:EmmaNguyen99/DSP_AT3_Group20.git
```

4. In terminal, set the current working directory to project folder.

_You do not need to worry about installing software/dependencies such as Postgres, Python, Streamlit, etc. because Dockerfile and DockerCompose file has instructions in how to setup from Dockerhub and create an environment to make application operational in your machine._

## How to Run the Program

1. Start Docker in your local machine
2. In terminal, type this command to initiate the program:

```bash
docker compose up -d
```

3. In terminal, type this command. You should have 2 containers running which are Postgres (postgres_at3) and Streamlit (streamlit_at3).

```bash
docker ps
```

4. Go to your browser and type **localhost:8501**

## Project Structure

- README.md: A file providing important information about the project such project description, project structure, setup and running the project guide, citations, etc.
- requirements.txt: A list of all packages required to run the project. The file is used by pip to install.
- Dockerfile: A file contains commands to build a Docker image that dockerizes the Streamlit application.
- docker-compose.yml: A file contains commands to run docker images and configure corresponding containers.
- app/
  - streamlit_app.py: Entry of the application that call functions to set page configuration, session state, and displays Database Connection Menu, Tabs, etc.
- src/
  - config.py: Set app's configuration, set session states and display session states.
  - database/
    - display.py: Display database connection menu, connect to the database, and display table selectbox.
    - logics.py: Define a PostgresConnector class that manages the connection to databases.
    - queries.py: SQL queries to get the list of tables, content of the selected table, and schema info of a specific table.
  - dataframe/
    - display.py: Display an overall information and schema information and content of a selected table.
    - logics.py: Define a Dataset class that manages a dataset loaded from Postgres.
    - queries.py: SQL queries to get a list of numeric columns, a list of text columns, a list of datetime columns and primary key of the selected table.
  - serie_date/
    - display.py: Display an overall information, bar chart of value frequency, and top 20 most frequent values of each columns of the selected table.
    - logics.py: Define a DateColumn class that manages a datetime column loaded from Postgres.
    - queries.py: SQL queries to get earliest date, number of weekend, and number of date '1900-01-01'.
  - serie_numeric/
    - display.py: Display an overall information, histogram chart of value frequency, and top 20 most frequent values of each columns of the selected table.
    - logics.py: Define a NumericColumn class that manages a numeric column loaded from Postgres.
    - queries.py: SQL queries to get the number of negative values, standard deviation, and number of unique values of each column of the selected table.
  - serie_text/
    - display.py: Display an overall information, bar chart of value frequency, and top 20 most frequent values of each columns of the selected table.
    - logics.py: Define a TextColumn class that manages a text column loaded from Postgres.
    - queries.py: SQL queries to get the number of missing values, mode, and number of records with only alphabetical characters of each columns of the selected table.
  - test/
    - test_database_queries.py: Unit tests for src/database/queries.py
    - test_database_logics.py: Unit tests for src/database/logics.py
    - test_dataframe_queries.py: Unit tests for src/dataframe/queries.py
    - test_dataframe_logics.py: Unit tests for src/dataframe/logics.py
    - test_serie_date_queries.py: Unit tests for src/serie_date/queries.py
    - test_serie_date_logics.py: Unit tests for src/serie_date/logics.py
    - test_serie_numeric_queries.py: Unit tests for src/serie_numeric/queries.py
    - test_serie_numeric_logics.py: Unit tests for src/serie_numeric/logics.py
    - test_serie_text_queries.py: Unit tests for src/serie_text/queries.py
    - test_serie_text_logics.py: Unit tests for src/serie_text/logics.py

## Citations

- Read the docs from PostgreSQL to query and understand different datatypes (numeric, text, date):
  https://www.postgresql.org/docs/13/index.html
- Read docs from Streamlit to understand how to build a web application:
  https://docs.streamlit.io/
- Read the docs from Docker to build Dockerfile and DockerCompose:
  https://docs.docker.com/engine/reference/builder/
  https://docs.docker.com/compose/compose-file/
- Read the docs from Pandas to extract and manipulate data:
  https://pandas.pydata.org/docs/
- Read the docs from Psycopg2 to execute operations to extract data:
  https://www.psycopg.org/docs/
- Read the docs from Python unittest to use Mock for testing:
  https://docs.python.org/3/library/unittest.mock.html
