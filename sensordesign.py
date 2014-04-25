from materials import simple_materials as materials
from sensing import get_image, create_grid, plot, Band

#####
## GENERATE REFLECTANCE CURVE PLOT
#####
plot(materials)


#####
## CREATE BANDS
#####

print("Create your bands.")

selection = None
band = 1
bands = []
while selection not in ['q', 'Q']:
    print("""Band creation options:
    1 - Create New Band
    Q - Quit and proceed
    """)

    if bands:
        print("Current Bands")
        for b in bands:
            print("Band Number {}: {}nm to {}nm".format(b.number,
                                                        b.start_lambda,
                                                        b.stop_lambda))
        print("")

    selection = raw_input("Enter a selection:")
    if selection == '1':
        start_lambda = float(raw_input("Enter starting wavelength in nm: "))
        stop_lambda = float(raw_input("Enter stop wavelength in nm: "))
        print("Creating a band.")
        bands.append(Band(band, start_lambda, stop_lambda))
        band += 1

print("Bands created!\n")


#####
## SHADE BANDS ON REFLECTANCE PLOT
#####
plot(materials, bands, show_bands=True)

#####
## GENERATE PIXEL VALUES
#####
test_data = create_grid(materials, mixed=True, constrained=False)
test_image = get_image(test_data, bands)

print("Remotely Sensed Image for Interpretation\n")
for x in range(3, 10, 3):
    print(test_image[x-3:x])


raw_input("""Press any key to reveal materials.\n""")
for x in range(3, 10, 3):
    print([m.name for m in test_data][x-3:x])



