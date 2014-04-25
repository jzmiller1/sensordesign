import random
from collections import namedtuple

import pylab
import scipy.integrate as integrate


Band = namedtuple('Band', ['number', 'start_lambda', 'stop_lambda'])


def sense(start_lambda, stop_lambda, reflectance_curve):
    """Returns reflectance value for a given material."""
    avg = 1.0 / (stop_lambda - start_lambda)
    I = integrate.quad(reflectance_curve, start_lambda, stop_lambda)
    return round(avg * I[0])


def get_image(terrain, bands):
    """Returns remotely sensed image for given bands and terrain."""
    image = []
    for pixel in terrain:
        pixel_values = []
        for band in bands:
            band_value = sense(band.start_lambda,
                               band.stop_lambda,
                               pixel.reflectance_curve)
            pixel_values.append(band_value)
        image.append(pixel_values)
    return image


def create_grid(materials, size=9):
    """Returns a list of pixels.

    Material in the pixel is chosen at random from materials.

    """

    pixels = []
    for x in range(size):
        m = random.choice(materials.keys())
        pixels.append(materials[m])
    return pixels


def plot(materials, bands=False, show_bands=False, show_fit_eqn=False):

    def color_region(x1, x2, color='orange'):
        """Color a specified region of a plot."""
        pylab.axvspan(x1, x2, facecolor=color, alpha=0.6)

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
        pylab.plot(range(400, 1000, 5),
                   [m.reflectance_curve(x) for x in range(400, 1000, 5)],
                   '--',
                   label=m.name)

    pylab.title('Reflectance Curves')
    pylab.xlabel('Wavelength (nm)')
    pylab.ylabel('% Reflectance')
    pylab.legend()
    #pylab.text(425, 11, poly2latex(c, width=16), fontsize=10)

    pylab.gcf().canvas.set_window_title('Sensor Design')


    if bands and show_bands:
        pylab.title('Reflectance Curves with Your Sensor Bands')
        for num, start_lambda, stop_lambda in bands:
            color_region(start_lambda, stop_lambda)

    pylab.show()