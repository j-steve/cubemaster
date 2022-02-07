from cube import Cube
from face import Rotation
import time
import copy
import random

_ROTATIONS = [Rotation.LEFT, Rotation.UP, Rotation.COUNTERCLOCKWISE]
_OFFSETS = [0, 1, 2]
_MAX_UNIFORMITY_SCORE = 108  # 72 #102
_MAX_ROTATIONS_PER_STEP = 14  # the largest number of rotations per step we can calculate before running out of memory.


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
        last_uniformity_score = initial_uniformity_score
        best_uniformity_score = initial_uniformity_score
        reverts = 0
        iterations = 0
        total_rotations = 0
        total_rotate_calc_time = 0
        risk_tolerance = 0.0
        while iterations < 1000000000000000:
            iterations += 1
            rotations_per_iteration = 0
            iteration_uniformity_score = last_uniformity_score
            ranked_cubes = {}
            print('Rotating: ', end='', flush=True)
            while iteration_uniformity_score <= last_uniformity_score and rotations_per_iteration < _MAX_ROTATIONS_PER_STEP:
                rotations_per_iteration += 1
                print('.', end='', flush=True)
                if rotations_per_iteration % 5 == 0:
                    print(' ', end='', flush=True)
                for cube in self._rotate_x_times(self.cube, rotations=0, target_rotations=rotations_per_iteration):
                    uniformity_score = cube.get_uniformity_score()
                    if cube == self.cube:
                        continue
                    if uniformity_score not in ranked_cubes:
                        ranked_cubes[uniformity_score] = []
                    ranked_cubes[uniformity_score].append(cube)
                iteration_uniformity_score = max(ranked_cubes.keys())
            print()
            total_rotations += rotations_per_iteration
            if iteration_uniformity_score > best_uniformity_score:
                best_uniformity_score = iteration_uniformity_score
            elif iteration_uniformity_score <= last_uniformity_score:
                pass
                # we weren't able to find a more optimum solution.  To prevent getting stuck in a local optimum,
                # choose a new cube at random.
                #print('Picking random cube to prevent getting stuck in local optimum.')
                #iteration_uniformity_score = random.choice(list(ranked_cubes.keys()))
            self.cube = ranked_cubes[iteration_uniformity_score][0]
            last_uniformity_score = iteration_uniformity_score
            if iterations % 1 == 0:
                print(
                    'Iteration #%s | (%s rotations | %s rotations/iteration | uniformity %i%% | best %i%% | initial %i%%)' % (
                        iterations, total_rotations, rotations_per_iteration,
                        iteration_uniformity_score / _MAX_UNIFORMITY_SCORE * 100,
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
