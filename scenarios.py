import copy

from materials import three_materials, two_materials
import sensing as rs


class Scenario():
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
        self.terrain = rs.create_grid(self.materials,
                                      mixed=mixing,
                                      constrained=constrained)

    def display(self):
        print("Remotely Sensed Image for Interpretation\n")
        for x in range(3, 10, 3):
            print(self.image[x-3:x])

        raw_input("""Press any key to reveal terrain.\n""")
        for x in range(3, 10, 3):
            print([m.name for m in self.terrain][x-3:x])
        raw_input("""Press any key to end scenario.\n""")

    def execute(self):
        ## GENERATE REFLECTANCE CURVE PLOT
        print("Start by reviewing the reflectance curves.")
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



scenarii = [Scenario('Two Materials', two_materials),
            Scenario('Three Materials', three_materials),
            Scenario('Constrained Linear Spectral Mixing',
                     two_materials,
                     spectral_mixing={'mixing': True,
                                      'constrained': True}),
            Scenario('Unconstrained Linear Spectral Mixing',
                     two_materials,
                     spectral_mixing={'mixing': True,
                                      'constrained': False})]


