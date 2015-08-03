from scenarios import scenarii, view_spectrum
import sensing
from materials import Material, create_db, find_and_load_data
import os


try:
    BASE_DIR = os.path.dirname(__file__)
except NameError:
    import sys
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


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
    file_list = []
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for file in files:
            file_list.append(file)
    if 'data.db' not in file_list:
        print('We need to load the initial data.')
        print('Ensure that data files are located in the data subfolder.')
        print('\n')
        print('Please select option: \n'
              '1 - Build Database\n'
              'Q - Quit\n')
        selection = raw_input('Enter Selection: ')
        print('\n')
        if selection.isdigit() and selection in ['1']:
            selection = None
            create_db()
            find_and_load_data(BASE_DIR)
    else:
        break

# Menu option functions for Sensor Design

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
    menu_count += 1
    print("{} - Reload Data".format(menu_count))
    print("Q - Quit")

    selection = raw_input("Enter a selection: ")
    print('\n')
    if selection.isdigit() and selection in valid_scenarios:
        scenario = scenarii[int(selection)-1]
        print("Launching {}".format(scenario.name))
        scenario.execute()
    # This is not going to work if the number of scenarios increases
    elif selection.isdigit() and selection == '5':
        view_spectrum()
    elif selection.isdigit() and selection == '6':
        print('Database Detected')
        print('Are you sure you want to reload the data?')
        print('\n')
        print('Please select option: \n'
              '1 - Yes, Rebuild Database\n'
              'Q - No, Return to Main Menu\n')
        selection = raw_input('Enter Selection: ')
        print('\n')
        if selection.isdigit() and selection in ['1']:
            os.remove(os.path.join(BASE_DIR, 'data.db'))
            create_db()
            find_and_load_data(BASE_DIR)
        elif selection in ['Q', 'q']:
            exit = 'C'
            selection = None

print("Done!\n")

