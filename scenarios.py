import sqlite3
import copy
from materials import Material, three_materials, two_materials
import sensing as rs


class Scenario():
    """This class models a given remote sensing scenario as defined by the
    number of materials involved and mixing within pixels. Mixing can be
     constrained (static percentage values for mixing) or unconstrained
     (random percentage values for mixing).

    """
    def __init__(self, name, materials,
                 terrain=None,
                 atmosphere=None,
                 spectral_mixing=False,
                 ):
        self.name = name
        self.materials = copy.deepcopy(materials)
        self.base_materials = copy.deepcopy(materials)
        self.terrain = terrain
        self.atmosphere = atmosphere
        self.spectral_mixing = spectral_mixing
        if not self.spectral_mixing:
            self.spectral_mixing = {'mixing': False, 'constrained': True}

    def generate_terrain(self, mixing=False, constrained=True):
        #Generates a 3x3 grid of remotely sensed pixel values based
        #on Scenario parameters and stores them in self.terrain.
        self.terrain = rs.create_grid(self.materials,
                                      mixed=mixing,
                                      constrained=constrained)

    def display(self):
        #displays pixel values from self.terrain for user interpretation
        #then displays materials and percentages which yielded those values.
        print("Remotely Sensed Image for Interpretation\n")
        for x in range(3, 10, 3):
            print(self.image[x-3:x])
        print('\n')
        raw_input("""Press any key to reveal terrain.\n""")
        for x in range(3, 10, 3):
            print([m.name for m in self.terrain][x-3:x])
        print('\n')
        raw_input("""Press any key to end scenario.\n""")

    def execute(self):
        ## GENERATE REFLECTANCE CURVE PLOT
        print("Start by reviewing the reflectance curves.\n")
        rs.plot(self.base_materials)

        ## CREATE BANDS
        print("Create your bands.")
        bands = rs.create_bands()

        ## SHADE BANDS ON REFLECTANCE PLOT
        rs.plot(self.base_materials, bands, show_bands=True)

        ## GENERATE PIXEL VALUES
        if self.terrain is None:
            self.generate_terrain(self.spectral_mixing['mixing'],
                                  self.spectral_mixing['constrained'])
        self.image = rs.get_image(self.terrain, bands)

        self.display()


def view_spectrum():
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
        rs.plot({'material': Material(materials[int(spectrum)])})


scenarii = [Scenario('Two Materials', two_materials),
            Scenario('Three Materials', three_materials),
            Scenario('Constrained Linear Spectral Mixing',
                     two_materials,
                     spectral_mixing={'mixing': True,
                                      'constrained': True}),
            Scenario('Unconstrained Linear Spectral Mixing',
                     two_materials,
                     spectral_mixing={'mixing': True,
                                      'constrained': False})
            ]


