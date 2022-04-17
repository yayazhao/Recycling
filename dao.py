import sqlite3
from typing import List

class R3Dao():

    def __init__(self):
        # Connect to database
        self.connection = sqlite3.connect("r3.db")
        self.cursor = self.connection.cursor()

    def get_waste_types(self):
        self.cursor.execute("SELECT distinct Category FROM '.\\WasteTypes';")
        categories = self.cursor.fetchall()
        self.cursor.execute("SELECT distinct Waste FROM '.\\WasteTypes';")
        waste_types = self.cursor.fetchall()
        waste_types = categories + waste_types
        waste_types = [row[0] for row in waste_types]
        return waste_types

    def search_reuse(self, goods: str = '',
                     goal: str = 'Donate',
                     min_lon: float = None,
                     max_lon: float = None,
                     min_lat: float = None,
                     max_lat: float = None) -> List[str]:
        '''
        :param goods:
        :param goal: 'Buy' or 'Donate'
        :return:
        '''
        goal_phrase = "r.AcceptDonation == 'Y'" if goal == 'Donate' \
                 else "r.Sell == 'Y'" if goal == 'Buy' else ''
        goal_phrase = f"AND {goal_phrase}" if goal_phrase else ""
        gps_phrase = f"AND Lng > {min_lon} AND Lng < {max_lon} AND Lat > {min_lat} AND Lat < {max_lat}" \
                     if min_lon is not None and max_lon is not None and min_lat is not None and max_lat is not None \
                     else ''
        self.cursor.execute(f"""
            SELECT distinct r.ID, r.Name, r.Phone, r.Street, r.City, r.State, r.Zip, r.Lat, r.Lng FROM '.\\NcOrangeReuseList' as r
                 WHERE (r.Goods like '%All%' OR r.Goods like '%{goods}%') {goal_phrase} {gps_phrase}""")
        return self.cursor.fetchall()

    def search_recycle_by_category(self, category: str,
                                   min_lon: float = None,
                                   max_lon: float = None,
                                   min_lat: float = None,
                                   max_lat: float = None) -> List[str]:
        gps_phrase = f"AND Lng > {min_lon} AND Lng < {max_lon} AND Lat > {min_lat} AND Lat < {max_lat}" \
            if min_lon is not None and max_lon is not None and min_lat is not None and max_lat is not None \
            else ''
        self.cursor.execute(f"""
            SELECT distinct s.ID, s.Name, s.Phone, s.Street, s.City, s.State, s.Zip, s.Lat, s.Lng FROM '.\\WasteTypes' as w
                     JOIN '.\\NcRecyclingSiteWasteType' as sw
                       on w.key = sw.WasteKey
                     JOIN '.\\NcRecylingList' as s
                       on s.key = sw.SiteKey
                     WHERE w.Category like '%{category}%' {gps_phrase};""")
        return self.cursor.fetchall()

    def search_recycle_by_waste(self, waste: str,
                                min_lon: float = None,
                                max_lon: float = None,
                                min_lat: float = None,
                                max_lat: float = None) -> List[str]:
        gps_phrase = f"AND Lng > {min_lon} AND Lng < {max_lon} AND Lat > {min_lat} AND Lat < {max_lat}" \
            if min_lon is not None and max_lon is not None and min_lat is not None and max_lat is not None \
            else ''
        self.cursor.execute(f"""
            SELECT distinct s.ID, s.Name, s.Phone, s.Street, s.City, s.State, s.Zip, s.Lat, s.Lng FROM '.\\WasteTypes' as w
                     JOIN '.\\NcRecyclingSiteWasteType' as sw
                       on w.key = sw.WasteKey
                     JOIN '.\\NcRecylingList' as s
                       on s.key = sw.SiteKey
                     WHERE w.Waste like '%{waste}%' {gps_phrase};""")
        return self.cursor.fetchall()

# dao = R3Dao()
# print(len(dao.search_reuse(goal='Buy', min_lon=-82, max_lon=-78, min_lat=35, max_lat=37)))
# print(len(dao.search_reuse(goal='Donate', min_lon=-82, max_lon=-78, min_lat=35, max_lat=37)))
# print(len(dao.search_recycle_by_waste('plastic', min_lon=-79.1, max_lon=-78, min_lat=35, max_lat=37)))
# print(len(dao.search_recycle_by_waste('', min_lon=-79.1, max_lon=-78, min_lat=35, max_lat=37)))
# print(len(dao.search_recycle_by_waste('plastic')))
# print(len(dao.search_recycle_by_waste('cartridge')))
#
# print(len(dao.search_recycle_by_category('garden', min_lon=-79.1, max_lon=-78, min_lat=35, max_lat=37)))
# print(len(dao.search_recycle_by_category('', min_lon=-79.1, max_lon=-78, min_lat=35, max_lat=37)))
# print(len(dao.search_recycle_by_category('garden')))
# print(len(dao.search_recycle_by_category('')))