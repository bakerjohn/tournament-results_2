#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament") # connect to the database called tournament


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()# connect to the database
    c = db.cursor()# establish a cursor to run queries and fetch results
    c.execute("DELETE FROM Matches;")# delete all data from the Matches table
    db.commit()# commit the change to the database
    db.close() # close the connection  


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM Players;")
    db.commit()
    db.close()    


def countPlayers():
    """Returns the number of players currently registered.
        
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM Players;")#count the number of players in the ID column
    num = c.fetchone()[0]
    db.close()
    return num # Return the results
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) values (%s)",(name,))# Insert into the players table a new name
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT id,name,wins,matches FROM playerstandings ORDER BY wins DESC;")# select the information for the view called Playerstandings
    rows = c.fetchall() # fetch all the information
    db.close()
    return rows # return the information in rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO Matches(winner, loser) VALUES (%s,%s)", (winner, loser, ))# insert in to the matches table values for winner and loser
    db.commit()
    db.close() 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    The for loop below is looping through the standings table and taking every second
    row and placing it in a tuple list of (id1, name1, id2, name2) and goes through all the 
    players in the tournament - only taking account for even amount of players.

    
  
  1. You can use the list type to implement simple data structures, such as stacks and queues. http://effbot.org/zone/python-list.htm
  2. Looping technique. Return an enumerate object https://docs.python.org/2/library/functions.html#enumerate
  3. Append -Add an item to the end of the list https://docs.python.org/2/tutorial/datastructures.html
  4. The for-in statement makes it easy to loop over the items in a list: http://effbot.org/zone/python-list.htm
"""

    db = connect()
    c = db.cursor()

    pairings = [] # Input list.
    
    c.execute("SELECT * FROM playerstandings")
    players = c.fetchall()
    

    
    # For loops are traditionally used when you have a piece of code which you want to repeat n number of times. turorials http://www.dotnetperls.com/list-python
        
    for i in range(0,len(players) - 1,2):
        
     # iterate over the indices of a sequence, combine range() and len() 
     #  #Iterate over each of the players by 2, and pair them    
        pairing = (players[i][0], players[i][1], players[i+1][0],players[i+1][1])
     # and another element to te end of the list at the end of the loop   
        pairings.append(pairing)
     
    return pairings
