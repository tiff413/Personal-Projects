import pandas as pd

# INPUTS
a = 3   # Enter number of streaming history files
folderName = "myData"
absPath = "/Users/tiffanyyu/Desktop/cs/mySpotifyData/"

# CREATE MASTER DF
allData = pd.DataFrame(columns=["artistName","endTime","msPlayed","trackName"])
# READ IN ALL STREAMING HISTORY FILES AND APPEND TO MASTER DF
for i in range(a):
    fileData = pd.read_json(absPath+folderName+"/StreamingHistory"+str(i)+".json", orient='columns')
    allData = allData.append(fileData, ignore_index=True)

# TOTAL LISTENING HOURS:
allData["msPlayed"].sum()/(1000*60*60)

#===============================================================================
# FIND MOST LISTENED TO ARTISTS

# CALCULATE (SONG) PLAYS PER ARTIST (ONLY COUNTS IF PLAY >= 15 SECONDS)
validPlaysData = allData.drop(allData[allData["msPlayed"]<15000].index)         # Select valid data, drop songsl played for under 15 secs
playsData = validPlaysData.groupby("artistName").size().reset_index(name="plays") # Count no. of rows/plays and make this a column

# COUNT AGGREGATE LISTENING TIME FOR EVERY ARTIST
artistData = allData[["artistName","msPlayed"]].groupby("artistName")           # Group by artist (make artist the index)
artistData = artistData.sum()[["msPlayed"]]                                     # Calculate aggregate milliseconds played per artist
artistData = artistData.merge(playsData, on=["artistName"])                     # Merge play data to get plays and aggregate time in the same df
artistData["hoursPlayed"] = artistData["msPlayed"]/(1000*60*60)                 # Create new column for hours played
artistData = artistData.drop(columns=["msPlayed"])                              # Drop column for milliseconds played

# SORT ARTISTS BY LONGEST LISTENING TIME
artistDataByHours = artistData.sort_values(by="hoursPlayed", ascending=False)   # Sort artists by descending listening time
artistDataByHours = artistDataByHours.reset_index(drop=True)                    # Reset index

artistDataByHours

# SORT ARTISTS BY MOST NUMBER OF SONG PLAYS
artistDataByPlays = artistData.sort_values(by="plays", ascending=False)         # Sort artists by descending number of plays
artistDataByPlays = artistDataByPlays.reset_index(drop=True)                    # Reset index

artistDataByPlays

# SAVE RESULTS TO A CSV FILE
# artistDataByPlays.to_csv(folderName+"/artistDataByPlays.csv")

#-------------------------------------------------------------------------------
# SEARCH ARTIST
searchArtist = "The Vaccines"

artistDataByHours[artistDataByHours["artistName"]==searchArtist]

#===============================================================================
# FIND MOST LISTENED TO SONGS

# CALCULATE NUMBER OF PLAYS PER SONG (ONLY COUNTS IF PLAY >= 15 SECONDS)
validPlaysData = allData.drop(allData[allData["msPlayed"]<15000].index)         # Select valid data, drop songsl played for under 15 secs
playsData = validPlaysData.groupby(["trackName","artistName"]).size().reset_index(name="plays") # Count no. of rows/plays and make this a column

# CALCULATE AGGREGATE LISTENING TIME FOR EVERY SONG
songData = allData[["trackName","artistName","msPlayed"]].groupby(["trackName","artistName"]) # Group by track name and artist (make these the indices)
songData = songData.sum()[["msPlayed"]]                                         # Sum total milliseconds played
songData = songData.merge(playsData, on=["trackName","artistName"])             # Merge play data to get plays and msPlayed in the same df
songData["hoursPlayed"] = songData["msPlayed"]/(1000*60*60)                     # Create new column for hours played
songData = songData.drop(columns=["msPlayed"])                                  # Drop column for milliseconds played

# SORT SONGS BY LONGEST LISTENING TIME
songDataByHours = songData.sort_values(by="hoursPlayed", ascending=False)       # Sort songs by descending listening time
songDataByHours = songDataByHours.reset_index(drop=True)                        # Reset index

songDataByHours

# SORT SONGS BY MOST NUMBER OF PLAYS
songDataByPlays = songData.sort_values(by="plays", ascending=False)             # Sort songs by descending number of plays
songDataByPlays = songDataByPlays.reset_index(drop=True)                        # Reset index

songDataByPlays

# SAVE RESULTS TO A CSV FILE
# songDataByPlays.to_csv(fileName+"/songDataByPlays.csv")

#-------------------------------------------------------------------------------
# SEARCH ARTIST
searchArtist = "Elton John"

songDataByPlays[songDataByPlays["artistName"]==searchArtist]

#-------------------------------------------------------------------------------
# SEARCH SONG
searchSong = "Eternal Flame"

songDataByPlays[songDataByPlays["trackName"]==searchSong]

#-------------------------------------------------------------------------------
# SEARCH SONG AND ARTIST
searchSong = "Under Control"
searchArtist = "The Strokes"

songDataByPlays[(songDataByPlays["trackName"]==searchSong) & (songDataByPlays["artistName"]==searchArtist)]
