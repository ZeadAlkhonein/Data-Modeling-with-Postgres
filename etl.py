import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from datetime import datetime



def process_song_file(cur, filepath):
    """ 
    takes file song and insert it into the DB. 

    this function takes a file and convert it into dataframe and then insert the Data frame into the database 
    insert into table songs and artist. 

    Parameters: 
    cur: crusor of the DB
    filepath: path of file

    Returns: 
    nothing 

    """
    
    
    # open song file
    df = pd.read_json(filepath,lines=True)
    new_df = df.copy()
    new_df.head()

    # insert song record
    songs = df[['song_id','title','artist_id','year','duration']].dropna()
    print('111111')
    song_data = songs.loc[0]
    #print([song_data[0],song_data[1],song_data[2],song_data[3],song_data[4]])
    song_data = [song_data[0],song_data[1],song_data[2],int(song_data[3]),song_data[4] ]
    #cur.execute(song_table_insert, song_data)
    
    # insert artist record
    #print(new_df.head())
    artist_columns = ['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']
    artist_data = new_df[artist_columns]
    artist_list=list(artist_data.loc[0])
    cur.execute(artist_table_insert, artist_list)


def process_log_file(cur, filepath):
    """ 
    takes file logs and insert the data it into the DB. 

    this function takes a file and convert it into dataframe and then insert the Data frame into the database 
    insert into table time, songsplay and users. 

    Parameters: 
    cur: crusor of the DB
    filepath: path of file

    Returns: 
    nothing 

    """
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df.loc[df['page']=='NextSong']


    # convert timestamp column to datetime
    t = df['ts'].apply(lambda x : datetime.fromtimestamp(x/1000.0))

    start_time=df['ts']
    hour = t.dt.hour
    day = t.dt.day
    weekofyear = t.dt.weekofyear
    month = t.dt.month
    year = t.dt.year
    dayofweek = t.dt.dayofweek
    # insert time data records
    time_data = list(zip(start_time,hour,day,weekofyear,month,year,dayofweek))
    column_labels = ('start_time','hour','day','weekofyear','month','year','dayofweek')
    time_df = pd.DataFrame(data=time_data,columns=column_labels)


    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

  # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

  # insert songplay records
    for index, row in df.iterrows():
        
      # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

      # insert songplay record
        songplay_data = (index,row.ts,songid, artistid,row.level,row.sessionId,row.location,row.userAgent,row.userId)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ 
    gets all file in the data folder and the count it run the specific function
    
    Parameters: 
    cur: crusor of the DB
    conn : connection of the DB
    filepath: path of file
    func : type of function from the class

    Returns: 
    nothing 

    """
    
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    print("Done")
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    print("Done phase2")

    conn.close()


if __name__ == "__main__":
    main()