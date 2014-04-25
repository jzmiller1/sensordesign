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
            if pixel.purity == (100, 0):
                band_value = sense(band.start_lambda,
                                   band.stop_lambda,
                                   pixel.reflectance_curve)
                pixel_values.append(band_value)
            else:
                a1, a2 = pixel.purity
                i1 = sense(band.start_lambda,
                           band.stop_lambda,
                           pixel.reflectance_curve)
                i2 = sense(band.start_lambda,
                           band.stop_lambda,
                           pixel.other.reflectance_curve)
                pixel_values.append((a1/100.0 * i1) + (a2/100.0 * i2))
        image.append(pixel_values)
    return image


def create_grid(materials, size=9, mixed=False):
    """Returns a list of pixels.

    Mixed can only be true if length of materials is two.

    Material in the pixel is chosen at random from materials.

    """
    pixels = []
    if len(materials) > 2:
        mixed = False
    else:
        material_names = materials.keys()
        material_names.sort()
        first_material = materials[material_names[0]]
        second_material = materials[material_names[1]]
        mixtures = first_material.mix(second_material)
        for mix in mixtures:
            print mix.other
            materials[mix.name] = mix
    for x in range(size):
        if mixed:
            m = random.choice(materials.keys())
        else:
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