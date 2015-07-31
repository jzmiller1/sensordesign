# data_creator is a stand-alone module that allows the user to generate
# materials for the Sensor Design application. The user will
# provide a material name and a list of reflectance values at sample
# wavelengths across the EM spectrum. This app will approximate a
# reflectance curve and output a .txt file of interpolated reflectance values
# in a standard USGS format which can be read by Sensor Design's database
# builder.
# NOTE: When selecting sample wavelength values, data_creator can only
# approximate an accurate reflectance curve between the min and max values
# supplied by the user. Beyond the min and max wavelengths, the reflectance
# curve may be wildly inaccurate. User should supply sample values spanning
# a range where accuracy is needed.
import pylab
import os


def load_samples():
    """This function generates a menu with two options
    1) Add wavelength and reflectance to sample
    Q) Quit
     If option 1 is selected, the user adds a wavelength in nanometers and then
     a reflectance value as a percentage. The function appends the wavelength
     and reflectance values as a tuple to the list variable 'data.' When the
     user is done entering sample pairs and enters option 'Q,' the function
     returns 'data.'"""
    selection = None
    menu_count = 1
    options = ['Add wavelength and reflectance to sample']
    data = []
    while selection not in ['q', 'Q']:
        print('Options: ')
        for option in options:
            print ('{} - {}'.format(menu_count, option))
            selection = raw_input('Choose option or Q to quit: ')
        if selection == '1':
            wavelength = float(raw_input('Please enter wavelength value in '
                                         'nanometers : '))
            reflectance = float(raw_input('Please enter reflectance value at '
                                          '{} nm: '.format(wavelength)))
            data.append((wavelength, reflectance))
    return data


def create_curve(data, polyfit_degree=7):
    """This function finds a best-fit curve for a list of data points.
    This function accepts a list argument 'data' as input and an integer
     polynomial degree of fit. The 'data' argument is a list of 2 item
     tuples (x, y). The polynomial degree of fit defaults to a 7th degree
     polynomial. The function returns the equation for the polynomial
     fit line."""
    reflectance_curve = pylab.polyfit([wavelength for wavelength,
                                       reflectance in data],
                                      [reflectance for wavelength,
                                       reflectance in data],
                                      polyfit_degree)
    return pylab.poly1d(reflectance_curve)


def return_reflectance(value, reflectance_curve):
    """Returns reflectance value for a given material. The inputs are a
    wavelength value and the reflectance curve function for a particular
    material"""
    return reflectance_curve(value)

# Code below initiates the data loading process by calling load_samples().
# Once a set of samples have been loaded, the code verifies that the samples
# are correct. If they are incorrect, load_samples is called again. If the
# samples are correct, the samples are passed to the create_curve() function
# and a best fit line and corresponding equation are generated. Using the
# best-fit equation, the remaining code creates a .txt file in the USGS format
# readable by Sensor Design's database builder containing an interpolated
# data set for a new material.
if __name__ == "__main__":
    choice = None
    samples = []
    print ('Get ready to load sample data')
    while choice not in ['Y', 'y']:
        samples = load_samples()
        print samples
        print ('Are these samples correct?')
        print ('Enter Y or y if they are correct ')
        choice = raw_input('Enter another key to restart if they are '
                           'incorrect: ')

    curve = create_curve(samples)
    filename = raw_input('Enter a filename: ')
    root = os.getcwd()
    filepath = ('{}/data/{}.txt'.format(root, filename))
    f = open(filepath, 'w')
    f.write('Spectral Data Creation Script\n')
    for each in range(0, 13):
        f.write('blank\n')
    f.write(raw_input('What material is this? '))
    f.write('\n')
    f.write('blank\n')
    for wl in range(350, 2501):
        rf = return_reflectance(wl, curve)
        a, b, c = wl/1000.0, rf/100.0, '0.000000'
        f.write('       {0:.6f}       {1:.6f}       {2}\n'.format(a, b, c))

    f.close()
