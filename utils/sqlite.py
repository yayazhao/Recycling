import pandas as pd
import sqlite3

"""
Convert .csv file to sqlite3 database table
"""

csv_file = '../facilities.csv'
con = sqlite3.connect('../facilities.db')
# df = pd.read_csv(csv_file)
# df.to_sql('SW_FacilityList_LatLng', con, if_exists='append', index=False)  # Solid Waste Facility List with Lat and Lng

all_results = con.execute('''select * from SW_FacilityList_LatLng''').fetchall()
print(all_results)
print(len(all_results))

all_results = con.execute('''select * from SW_FacilityList_LatLng WHERE lng > %s AND lng < %s AND lat > %s AND lat < %s''' % (-80.06, -78.06, 34.96, 36.96)).fetchall()
print(all_results)
print(len(all_results))

35.9680943,-79.08272099999999
