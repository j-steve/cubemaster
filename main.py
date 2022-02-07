# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from cube import Cube
from face import Rotation
from solver import Solver

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    cube = Cube()
    cube.print()
    print(cube.get_uniformity_score())
    cube.rotate(Rotation.RIGHT, 0)
    cube.print()
    #cube.rotate(Rotation.LEFT, 2)
    cube.rotate(Rotation.UP, 0)
    cube.print()
    cube.rotate(Rotation.UP, 0)
    cube.print()
    cube.rotate(Rotation.COUNTERCLOCKWISE, 0)
    cube.print()

    solver = Solver(cube)
    solver.randomize(10000)
    cube.print()
    # print("Press enter to solve...")
    #input()
    solver.solve()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
