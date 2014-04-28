from scenarios import scenarii


print("Welcome to Sensor Design.")

selection = None
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
    print("Q - quit")

    selection = raw_input("Enter a selection:")
    if selection.isdigit() and selection in valid_scenarios:
        scenario = scenarii[int(selection)-1]
        print("Launching {}".format(scenario.name))
        scenario.execute()

print("Done!\n")

