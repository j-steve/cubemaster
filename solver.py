from cube import Cube
from face import Rotation
import time
import copy
import random

_ROTATIONS = [Rotation.LEFT, Rotation.UP, Rotation.COUNTERCLOCKWISE]
_OFFSETS = [0, 1, 2]
_MAX_UNIFORMITY_SCORE =  108 #72 #102


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
        steps = 0
        uniformity_score = self.cube.get_uniformity_score()
        initial_uniformity_score = uniformity_score
        best_uniformity_score = uniformity_score
        reverts = 0
        iterations = 0
        total_rotate_calc_time = 0
        risk_tolerance = 0.0
        cube_copy = copy.deepcopy(self.cube)
        while steps < 1000000000000000:

            start_time = time.time()
            #risk_tolerance = random.random()  # likelihood of choosing a worse or neutral option vs a net improvement
            if risk_tolerance < 1:
                risk_tolerance += 0.000001
            #if len(self._permutations_to_skip) >= 9:
             #   risk_tolerance += 0.03
              #  self._permutations_to_skip.clear()

            #this_rotation = self._random_rotation()
            this_rotation = None
            for i in range(0, 20):
                self._random_rotation()
            total_rotate_calc_time += time.time() - start_time
            new_uniformity_score = self.cube.get_uniformity_score()
            iterations += 1

            if (new_uniformity_score < uniformity_score and risk_tolerance < 0.8) or (
                    new_uniformity_score == uniformity_score and risk_tolerance < 0.6):
                self._permutations_to_skip.add(this_rotation)
                self.cube = cube_copy
                reverts += 1
            else:
                cube_copy = copy.deepcopy(self.cube)
                risk_tolerance -= 0.5
                self._permutations_to_skip.clear()
                if new_uniformity_score > uniformity_score:
                    risk_tolerance = 0
                    if new_uniformity_score > best_uniformity_score:
                        best_uniformity_score = new_uniformity_score
                uniformity_score = new_uniformity_score
                steps += 1

            if iterations % 10000 == 0:
                print(
                    'Iteration #%s (uniformity %s | best %s | initial %s | risk tolerance %i.1%% | %s reverts | avg calc time: %.2gms)' % (
                        steps, uniformity_score, best_uniformity_score, initial_uniformity_score, risk_tolerance * 100, reverts,
                        total_rotate_calc_time / iterations * 1000))
                self.cube.print()
            if uniformity_score == _MAX_UNIFORMITY_SCORE:
                print("Solved in %s", steps)
                return
        print('Failed to solve after 1000000000000000 iterations.')
        cube.print()

    def _random_rotation(self):
        result = None
        while not result or result in self._permutations_to_skip:
            result = (random.choice(_ROTATIONS), random.choice(_OFFSETS))
        self.cube.rotate(result[0], result[1])
        return result
