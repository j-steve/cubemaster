from cube import Cube
from face import Rotation
import time
import copy
import random

_ROTATIONS = [Rotation.LEFT, Rotation.UP, Rotation.COUNTERCLOCKWISE]
_OFFSETS = [0, 1, 2]
_MAX_UNIFORMITY_SCORE = 108  # 72 #102
_ROTATIONS_PER_STEP = 15


class Solver(object):

    def __init__(self, cube: Cube):
        self.cube = cube
        self._permutations_to_skip = set()

    def randomize(self, iterations: int):
        for i in range(0, iterations):
            self._random_rotation()

    def solve(self):
        print('Solving...')
        # steps = []
        initial_uniformity_score = self.cube.get_uniformity_score()
        best_uniformity_score = initial_uniformity_score
        reverts = 0
        iterations = 0
        total_rotate_calc_time = 0
        risk_tolerance = 0.0

        while iterations < 1000000000000000:
            iterations += 1
            ranked_cubes = {}
            for cube in self._rotate_x_times(self.cube, rotations=0, target_rotations=_ROTATIONS_PER_STEP):
                uniformity_score = cube.get_uniformity_score()
                if uniformity_score not in ranked_cubes:
                    ranked_cubes[uniformity_score] = []
                ranked_cubes[uniformity_score].append(cube)
            iteration_uniformity_score = max(ranked_cubes.keys())
            self.cube = ranked_cubes[iteration_uniformity_score][0]
            if iteration_uniformity_score > best_uniformity_score:
                best_uniformity_score = iteration_uniformity_score
            if iterations % 1 == 0:
                print(
                    'Rotation #%s (uniformity %i%% | best %i%% | initial %i%%)' % (
                        iterations * _ROTATIONS_PER_STEP, iteration_uniformity_score / _MAX_UNIFORMITY_SCORE * 100,
                        best_uniformity_score / _MAX_UNIFORMITY_SCORE * 100,
                        initial_uniformity_score / _MAX_UNIFORMITY_SCORE * 100))
                self.cube.print()
            if uniformity_score == _MAX_UNIFORMITY_SCORE:
                print("Solved in %s", iterations)
                self.cube.print()
                return
        print('Failed to solve after 1000000000000000 iterations.')
        self.cube.print()

    def _rotate_x_times(self, cube: Cube, rotations: int, target_rotations: int):
        for rotation in _ROTATIONS:
            for offset in _OFFSETS:
                cube_copy = copy.deepcopy(cube)
                cube_copy.rotate(rotation, offset)
                rotations += 1
                if rotations < target_rotations:
                    for child_cube in self._rotate_x_times(cube_copy, rotations, target_rotations):
                        yield child_cube
                else:
                    yield cube_copy

    def _random_rotation(self):
        result = None
        while not result or result in self._permutations_to_skip:
            result = (random.choice(_ROTATIONS), random.choice(_OFFSETS))
        self.cube.rotate(result[0], result[1])
        return result
