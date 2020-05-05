# DROP TABLES

songplay_table_drop = "DROP TABLE if exists songplays"
user_table_drop = "DROP TABLE if exists users"
song_table_drop = "DROP TABLE if exists SONGS"
artist_table_drop = "DROP TABLE if exists artists"
time_table_drop = "DROP TABLE if exists time"

# CREATE TABLES

songplay_table_create = ("""create table if not exists songplays \
(songplay_id int NOT NULL,\
start_time varchar(50),\
song_id varchar(200),\
artist_id varchar(200),\
level varchar(50),\
session_id int NOT NULL,\
location varchar(50),\
user_agent varchar(200),\
user_id int NOT NULL,\
PRIMARY KEY (songplay_id)
)
""")

user_table_create = ("""
CREATE TABLE if not exists users \
(userid int NOT NULL,\
firstName varchar(200),\
lastName varchar(200),\
gender varchar(200),\
level varchar(200),\
PRIMARY KEY (userid)
)
""")

song_table_create = ("""
CREATE TABLE  IF NOT EXISTs SONGS\
(song_id varchar(200) NOT NULL,\
title varchar(200),\
artist_id varchar(200),\
year int,duration int,\
PRIMARY KEY (song_id))
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists\
(artist_id varchar(200) NOT NULL,\
artist_name varchar(200),\
artist_location varchar(200)\
,artist_latitude varchar(200),\
artist_longitude varchar(200),\
PRIMARY KEY (artist_id))
""")

time_table_create = ("""
CREATE TABLE if not exists time (start_time bigint NOT NULL,\
hour int ,\
day int ,\
weekofyear int,\
month int,\
year int ,\
dayofweek int)
""")

# INSERT RECORDS

songplay_table_insert = ("""
insert into songplays
values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING
""")

user_table_insert = ("""
INSERT INTO users 
(userid,firstName,lastName,gender,level) 
values (%s,%s,%s,%s,%s) 
ON CONFLICT (userid) DO UPDATE SET level = (EXCLUDED.level)
""")

song_table_insert = ("""
INSERT INTO SONGS 
VALUES(%s,%s,%s,%s,%s)
""")

artist_table_insert = ("""
INSERT INTO artists 
VALUES (%s,%s,%s,%s,%s) 
ON CONFLICT (artist_id) 
DO UPDATE SET 
(artist_location,artist_latitude ,artist_longitude ) = (EXCLUDED.artist_location,EXCLUDED.artist_latitude,EXCLUDED.artist_longitude)
""")


time_table_insert = ("""
INSERT INTO time values (%s,%s,%s,%s,%s,%s,%s) 
ON CONFLICT DO NOTHING
""")


# FIND SONGS

song_select = ("""
SELECT song_id, A.artist_id from songs A join artists B on A.artist_id=B.artist_id where A.title = %s\
and B.artist_name=%s and A.duration=%s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]