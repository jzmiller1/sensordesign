import pylab


class Material():
    """Represents material (reflectance data points and curve function)."""

    def __init__(self, data, name, polyfit_degree=7):
        self.data = data
        reflectance_curve = pylab.polyfit([wavelength for wavelength, reflectance in data],
                                          [reflectance for wavelength, reflectance in data],
                                          polyfit_degree)
        self.reflectance_curve = pylab.poly1d(reflectance_curve)
        self.name = name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "Material('{}')".format(self.name)


#####
## CONSTRUCT MATERIALS DATA
#####
concrete_data = [(400, 34), (500, 35), (600, 36), (700, 34), (800, 33),
                 (900, 33), (1000, 33)]
concrete = Material(concrete_data, 'concrete')

valubilium_data = [(400, 34), (450, 35), (500, 34), (600, 37), (700, 45),
                   (800, 40), (900, 15), (1000, 20)]
valubilium = Material(valubilium_data, 'valubilium')

sand_data = [(400, 6), (450, 8), (500, 10), (600, 21), (700, 27),
             (800, 32), (900, 34), (1000, 37)]
sand = Material(sand_data, 'sand')

materials = {'valubilium': valubilium,
             'concrete': concrete,
             'sand': sand}
