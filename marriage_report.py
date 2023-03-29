"""
Description:
 Generates a CSV reports containing all married couples in
 the Social Network database.

Usage:
 python marriage_report.py
"""
import os
import sqlite3
from create_relationships import db_path
import pandas as pd

def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()
    # print(married_couples)
    # Save all married couples to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)

def get_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, start_date) of married couples 
    """
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur2 = con.cursor()
    cur.execute('SELECT * FROM people')
    cur2.execute('SELECT * FROM relationships')
    all_people = cur.fetchall()
    all_relationships = cur2.fetchall()
    married = []
    
    for couple in all_relationships:
        start_date = couple[4]
        person1 = ''
        person2 = ''
        list_items = (person1,person2,start_date)
        if couple[3] == 'spouse':
            for people in all_people:
                if people[0] == couple[1]:
                    person1 = people[1]
                if people[0] == couple[2]:
                    person2 = people[1]
                list_items = (person1,person2,start_date)
            married.append(list_items)
    con.commit()
    con.close()
    return married

def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  

    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """
    # TODO: Function body
    data = []
    for i in married_couples:
        person1 = i[0]
        person2 = i[1]
        start_date = i[2]
        data.append([person1,person2,start_date])
    report_df = pd.DataFrame(data)
    header_row = ('Person 1', 'Person 2', 'Anniversary')
    report_df.to_csv(csv_path, index=False, header=header_row)
    return

if __name__ == '__main__':
   main()