## sqlalchemy-challenge

### Part 1: Analyse and Explore the Climate Data.
In this part of the challenge, a climate analysis is undertaken to help plan a trip to Honolulu, Hawaii. The following steps are taken to accomplish this task:

The files (climate_starter.ipynb and hawaii.sqlite) are provided and used for climate analysis and data exploration.

SQLAlchemy create_engine() function is used connect to the SQLite database.

SQLAlchemy automap_base() function is used to reflect the tables into classes, and then save references to the classes named station and measurement.

Python is linked to the database by creating an SQLAlchemy session.

### Part 2: Design a Climate App.
In this part of the challenge, a Flask API based on the queries developed in part 1, is designed. Flask is used to create the routes.
