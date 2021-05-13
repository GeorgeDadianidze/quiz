import requests
import json
import sqlite3

key = 'FbEbva7ZJw0w9htVHhontDan4REenYr2nzsY9bEf'
#requests ის მეთოდები (get,headers,status_code,text)
u = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-01-1&end_date=2015-01-8&api_key={key}')
res = u.json()
print(u.headers['Date'])
print(u.status_code)
print(u.text)



with open("asteroid.json", "w") as file:
    json.dump(res, file, indent=3)

#2015-01-05 ში პირველი მეტეორის id,name და დიამეტრი მეტრებში.
id = print(res['near_earth_objects']['2015-01-05'][0]['id'])
name = print(res['near_earth_objects']['2015-01-05'][0]['name'])
diamter = print(res['near_earth_objects']['2015-01-05'][0]['estimated_diameter']['meters'])

conn = sqlite3.connect('nasa.sqlite')
c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS meteorinfo
                  (id INTEGER,
                  name VARCHAR(30),
                  MINdiameterInKM FLOAT, MAXdiamterInKM FLOAT,
                  MINdiameterInM FLOAT, MAXdiameterInM FLOAT,
                  MINdiameterInMile FLOAT, MAXdiameterInMile FLOAT,
                  MINdiameterInFeet FLOAT, MAXdiameterInFeet FLOAT
                  );""")


#ნასას აპიდან წამოვიღე ინფორმაცია ასტეროიდების შესახებ რომლებიც დედამიწასთან ახლოს იყვნენ
#ბაზაში შევიტანე ამ ასტეროიდების id,name,მინ.ზომა(კმ,მეტრი,მილი,ფუტი) და მაქს.ზომა(კმ,მეტრი,მილი,ფუტი)

containerDates = []
everything = []
for each in res['near_earth_objects']:
    containerDates.append(each)
for i in range(0,len(containerDates)):
    for j in res['near_earth_objects'][containerDates[i]][0:-1]:
        id = j['id']
        name = j['name']
        MINdiameterInKM = j['estimated_diameter']['kilometers']['estimated_diameter_min']
        MAXdiameterInKM = j['estimated_diameter']['kilometers']['estimated_diameter_max']
        MINdiamterInM = j['estimated_diameter']['meters']['estimated_diameter_min']
        MAXdiamterInM = j['estimated_diameter']['meters']['estimated_diameter_max']
        MINdiamterInMile = j['estimated_diameter']['miles']['estimated_diameter_min']
        MAXdiamterInMile = j['estimated_diameter']['miles']['estimated_diameter_max']
        MINdiamterInFeet = j['estimated_diameter']['feet']['estimated_diameter_min']
        MAXdiamterInFeet = j['estimated_diameter']['feet']['estimated_diameter_max']
        row = (id, name, MINdiameterInKM, MAXdiameterInKM, MINdiamterInM, MAXdiamterInM, MINdiamterInMile, MAXdiamterInMile, MINdiamterInFeet, MAXdiamterInFeet)
        everything.append(row)
c.executemany("""INSERT INTO meteorinfo
            (id, name,
            MINdiameterInKM, MAXdiamterInKM,
            MINdiameterInM, MAXdiameterInM,
            MINdiameterInMile, MAXdiameterInMile,
            MINdiameterInFeet, MAXdiameterInFeet) 
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", everything)
conn.commit()
conn.close()

