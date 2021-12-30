import mysql.connector

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="oscar0405" #PUT YUR OWN PASSWORD HERE
)

mycursor = cnx.cursor()


mycursor.execute("CREATE DATABASE footballplayersdb")

import pandas as pd

mycsv = pd.read_csv("players_21.csv")
print(mycsv.head())

#cleaning + creation of new variable
mycsv['goalkeeperSkills'] = (mycsv['goalkeeping_handling'] + mycsv['goalkeeping_diving'] + mycsv['goalkeeping_kicking'] + mycsv['goalkeeping_positioning'] + mycsv['goalkeeping_reflexes']) / 5
mycsv['id'] = mycsv['sofifa_id']

mycsv = mycsv[mycsv['league_rank'].notna()]
mycsv['league_rank'] = mycsv['league_rank'].astype(int)

mycsv = mycsv[mycsv['release_clause_eur'].notna()]
mycsv = mycsv[mycsv['contract_valid_until'].notna()]
mycsv['release_clause_eur'] = mycsv['release_clause_eur'].astype(int)
mycsv['contract_valid_until'] = mycsv['contract_valid_until'].astype(int)

mycsv = mycsv[mycsv['pace'].notna()]
mycsv['pace'] = mycsv['pace'].astype(int)
mycsv['shooting'] = mycsv['shooting'].astype(int)
mycsv['passing'] = mycsv['passing'].astype(int)
mycsv['dribbling'] = mycsv['dribbling'].astype(int)
mycsv['defending'] = mycsv['defending'].astype(int)
mycsv['physic'] = mycsv['physic'].astype(int)
mycsv['goalkeeperSkills'] = mycsv['goalkeeperSkills'].astype(int)

mycsv['team_jersey_number'] = mycsv['team_jersey_number'].astype(str)
mycsv['nation_jersey_number'] = mycsv['nation_jersey_number'].astype(str)



playerTable = mycsv[['id', 'player_url', 'long_name', 'short_name', 'age', 'height_cm', 'weight_kg', 'nationality', 'club_name']]

teamTable = mycsv[['club_name', 'league_name', 'league_rank']]
teamTable = teamTable.drop_duplicates(subset=['club_name'])


playerContractTable = mycsv[['id', 'value_eur', 'wage_eur', 'release_clause_eur', 'joined', 'contract_valid_until', 'club_name']]


playerCharacteristicsTable = mycsv[['id', 'overall', 'potential', 'preferred_foot', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'goalkeeperSkills', 'player_traits']]
playerCharacteristicsTable = playerCharacteristicsTable.fillna("NoTraits")

playerSpecificationsTable = mycsv[['id', 'team_position', 'nation_position', 'team_jersey_number', 'nation_jersey_number']]
playerSpecificationsTable = playerSpecificationsTable.fillna("NoNumber")



mycursor.execute("USE footballplayersdb;")

mycursor.execute('CREATE TABLE IF NOT EXISTS teamInformation (club_name varchar(255) primary key, league_name varchar(255), league_rank int)')
cnx.commit()


for row in teamTable.itertuples():
    mycursor.execute('''
                INSERT INTO teamInformation (club_name, league_name, league_rank)
                VALUES (%s,%s,%s)
                ''',
                (row.club_name,
                 row.league_name,
                 row.league_rank)
                )
cnx.commit()


mycursor.execute('CREATE TABLE IF NOT EXISTS playerProfile (id int primary key, player_url varchar(255), long_name varchar(255), short_name varchar(255), age int, height_cm int, weight_kg int, nationality varchar(255), club_name varchar(255), FOREIGN KEY(club_name) REFERENCES teamInformation(club_name))')
cnx.commit()


for row in playerTable.itertuples():
    mycursor.execute('''
                INSERT INTO playerProfile (id, player_url, long_name, short_name, age, height_cm, weight_kg, nationality, club_name)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',
                (row.id,
                row.player_url,
                row.long_name,
                row.short_name,
                row.age,
                row.height_cm,
                row.weight_kg,
                row.nationality,
                row.club_name)
                )
cnx.commit()


mycursor.execute('CREATE TABLE IF NOT EXISTS playerSpecifications (id int primary key, team_position varchar(255), nation_position varchar(255), team_jersey_number varchar(10), nation_jersey_number varchar(10))')
cnx.commit()


for row in playerSpecificationsTable.itertuples():
    mycursor.execute('''
                INSERT INTO playerSpecifications (id, team_position, nation_position, team_jersey_number, nation_jersey_number)
                VALUES (%s,%s,%s,%s,%s)
                ''',
                (row.id,
                row.team_position,
                row.nation_position,
                row.team_jersey_number,
                row.nation_jersey_number)
                )
cnx.commit()


mycursor.execute('CREATE TABLE IF NOT EXISTS playerCharacteristics (id int primary key, overall int, potential int, preferred_foot varchar(10), pace int, shooting int, passing int, dribbling int, defending int, physic int, goalkeeper int, playerTraits TEXT)')
cnx.commit()


for row in playerCharacteristicsTable.itertuples():
    mycursor.execute('''
                INSERT INTO playerCharacteristics (id, overall, potential, preferred_foot, pace, shooting, passing, dribbling, defending, physic, goalkeeper, playerTraits)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',
                (row.id,
                row.overall,
                row.potential,
                row.preferred_foot,
                row.pace,
                row.shooting,
                row.passing,
                row.dribbling,
                row.defending,
                row.physic,
                row.goalkeeperSkills,
                row.player_traits)
                )
cnx.commit()


mycursor.execute('CREATE TABLE IF NOT EXISTS playerContract (id int primary key, value_eur int, wage_eur int, release_clause_eur int, join_date DATE, contract_valid_until int, club_name varchar(255), FOREIGN KEY(club_name) REFERENCES teamInformation(club_name))')
cnx.commit()


for row in playerContractTable.itertuples():
    mycursor.execute('''
                INSERT INTO playerContract (id, value_eur, wage_eur, release_clause_eur, join_date, contract_valid_until, club_name)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ''',
                (row.id,
                row.value_eur,
                row.wage_eur,
                row.release_clause_eur,
                row.joined,
                row.contract_valid_until,
                row.club_name)
                )
cnx.commit()


