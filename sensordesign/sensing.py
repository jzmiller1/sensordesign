import random
import sqlite3
import os
from collections import namedtuple
import matplotlib.pyplot as pyplot
from settings import BASE_DIR
Band = namedtuple('Band', ['number', 'start_lambda', 'stop_lambda'])


def sense(band, material):
    """Returns the average reflectance value for a material within a given
    bandwidth.

    """
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'data.db'))
    c = conn.cursor()
    c.execute("""SELECT AVG(reflectance)
                 FROM main
                 WHERE material = ? AND wavelength >= ? AND wavelength <= ? AND REFLECTANCE >= 0;""",
              (material, band.start_lambda, band.stop_lambda))
    data = c.fetchone()[0]
    if isinstance(data, (int, float)) is False:
        return 0
    else:
        return round(data, 4)



def get_image(terrain, bands):
    """Returns remotely sensed image for given bands and terrain."""
    image = []
    for pixel in terrain:
        pixel_values = []
        for band in bands:
            if pixel.purity == (100, 0):
                band_value = sense(band,
                                   pixel.name)
                pixel_values.append(band_value)
            else:
                a1, a2 = pixel.purity
                i1 = sense(band,
                           pixel.name.split(':')[0])
                i2 = sense(band,
                           pixel.other.name)
                pixel_values.append(round((a1/100.0 * i1) + (a2/100.0 * i2)))
        image.append(pixel_values)
    return image


def image_to_bands(image):
    """docstring

    >>> image_to_bands([[12, 13], [12, 13], [12, 13],
    ...                 [12, 13], [12, 13], [12, 13],
    ...                 [12, 13], [12, 13], [12, 13]
    ...                ])
    [[12, 12, 12, 12, 12, 12, 12, 12, 12], [13, 13, 13, 13, 13, 13, 13, 13, 13]]
    """
    band_count = len(image[0])
    bands = []
    for i in range(band_count):
        band = []
        for q in range(len(image)):
            band.append(image[q][i])
        bands.append(band)
    image = bands
    return image



def create_grid(materials, size=9, mixed=False, constrained=True):
    """Returns a list of pixels.

    Mixed can only be true if length of materials is two.

    Material in the pixel is chosen at random from materials.

    """
    pixels = []
    if mixed:
        material_names = materials.keys()
        material_names.sort()
        first_material = materials[material_names[0]]
        second_material = materials[material_names[1]]
        mixtures = first_material.mix(second_material, constrained)
        for mix in mixtures:
            materials[mix.name] = mix
    for x in range(size):
        m = random.choice(materials.keys())
        pixels.append(materials[m])
    return pixels


def create_bands():
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
        print('\n')
        selection = raw_input("Enter a selection:")
        if selection == '1':
            try:
                start_lambda = float(raw_input("Enter starting wavelength in nm: "))
            except ValueError:
                print("this is not a valid input!")
                create_bands()
            try:
                stop_lambda = float(raw_input("Enter stop wavelength in nm: "))
            except ValueError:
                print("this is not a valid input!")
                create_bands()
            print("Creating a band.\n")
            bands.append(Band(band, start_lambda, stop_lambda))
            band += 1

    print("Bands created!\n")
    return bands


def plot(materials, bands=False, show_bands=False):
    """Plots and displays the reflectance curves for a list of materials.
    If bands contains data and show_bands==True, it also displays colored
    vertical bars which depict the bandwidths stored in bands.

    """

    def color_region(x1, x2, color='orange'):
        """Color a specified region of a plot."""
        pyplot.axvspan(x1, x2, facecolor=color, alpha=0.6)

    def poly2latex(poly, variable="x", width=2):
        """http://stackoverflow.com/questions/23149155/printing-the-equation-of-the-best-fit-line"""
        t = ["{0:0.{width}f}"]
        t.append(t[-1] + " {variable}")
        t.append(t[-1] + "^{1}")

        def f():
            for i, v in enumerate(reversed(poly)):
                idx = i if i < 2 else 2
                yield t[idx].format(v, i, variable=variable, width=width)

        return "${}$".format("+".join(f()))

    for k in materials:
        m = materials[k]
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'data.db'))
        c = conn.cursor()
        c.execute("""SELECT wavelength, reflectance FROM main WHERE material=?;""",
                  (m.name,))
        data = c.fetchall()
        x = [wavelength for wavelength, reflectance in data]
        y = [reflectance for wavelength, reflectance in data]
        pyplot.plot(x,
                   y,
                   '--',
                   label=m.name)
        pyplot.ylim((0, 100))
    pyplot.title('Reflectance Curves')
    pyplot.xlabel('Wavelength (nm)')
    pyplot.ylabel('% Reflectance')
    pyplot.legend()

    pyplot.gcf().canvas.set_window_title('Sensor Design')

    if bands and show_bands:
        pyplot.title('Reflectance Curves with Your Sensor Bands')
        for num, start_lambda, stop_lambda in bands:
            color_region(start_lambda, stop_lambda)

    pyplot.show()
    pyplot.clf()


if __name__ == '__main__':
    import doctest
    doctest.testmod()