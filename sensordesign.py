from scenarios import scenarii
import sqlite3
import sensing
from materials import Material, read_data, create_db
import os

BASE_DIR = os.path.dirname(__file__)

print("Welcome to Sensor Design.")

selection = None
exit = None

### This section of code will look for the database data.db.
###
### If data.db exists,it will prompt the user and ask if the database should
### be rebuilt or if it it is current. If it is current, the program will
### continue. If the user opts to rebuild the database, data.db will be deleted
### and the user will be prompted to build a new database.
###
### If data.db does not exist, the user will be prompted to build a database
### from the files in /data or exit the program.

while selection not in ['q', 'Q'] and exit is None:
    file_list=[]
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for file in files:
            file_list.append(file)
    if 'data.db' not in file_list:
        print('Sensor Design needs to build a database')
        print('Please make sure there are data files in data directory.')
        print('\n')
        print('Please select option: \n'
              '1 - Build Database\n'
              'Q - Quit\n')
        selection = raw_input('Enter Selection: ')
        print('\n')
        if selection.isdigit() and selection in ['1']:
            selection = None
            create_db()
            for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'data'),
                                             topdown=False):
                for name in files:
                    if name[-3:] == 'txt':
                        path = os.path.join(root, name)
                        read_data(path)

    else:
        print('Database Detected')
        print('Is the database loaded with current data?')
        print('\n')
        print('Please select option: \n'
              '1 -  No, Rebuild Database\n'
              'Q - Yes, please continue\n')
        selection = raw_input('Enter Selection: ')
        print('\n')
        if selection.isdigit() and selection in ['1']:
            os.remove(os.path.join(BASE_DIR, 'data.db'))
        elif selection in ['Q', 'q']:
            exit = 'C'
            selection = None

### This section of the code starts the menu option functions for Sensor
### Design.

band = 1
bands = []
valid_scenarios = [str(choice) for choice in
                   range(0, len(scenarii) + 1)]
while selection not in ['q', 'Q']:
    print("Scenario options:\n")
    menu_count = 1
    for s in scenarii:
        print("{} - {}".format(menu_count, s.name))
        menu_count += 1
    print("{} - View Spectrum".format(menu_count))
    print("Q - quit")

    selection = raw_input("Enter a selection: ")
    print('\n')
    if selection.isdigit() and selection in valid_scenarios:
        scenario = scenarii[int(selection)-1]
        print("Launching {}".format(scenario.name))
        scenario.execute()
    elif selection.isdigit() and selection == '5':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        materials = c.execute("""SELECT DISTINCT material FROM main ORDER BY material;""")
        materials = dict(enumerate([material[0] for material
                                    in materials.fetchall()], start=1))
        print("Select a Material:")
        for number, material in materials.items():
            print ('{} - {}'.format(number, material))
        spectrum = raw_input("Enter Selection: ")
        print('\n')
        if spectrum.isdigit() and int(spectrum) in materials.keys():
            sensing.plot({'material': Material(materials[int(spectrum)])})

print("Done!\n")

