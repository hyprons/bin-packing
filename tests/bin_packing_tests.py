import unittest

from bin_packing import compute_rotation


class RotationTests(unittest.TestCase):
    def test_rotations(self):
        dim = [0.5, 0.4, 0.3]
        rotations = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1)]
        # resultant rotation indexes
        pre_computed_rotations = [
            [0, 1, 2],
            [0, 2, 1],
            [2, 1, 0],
            [1, 0, 2],
            [2, 0, 1],
            [1, 2, 0],
        ]

        for idx, rot in enumerate(rotations):
            new_rot = compute_rotation(dim=dim, rot=rot)

            for i in range(3):
                print(dim[i], new_rot[pre_computed_rotations[idx][i]], new_rot, rot)
                # check whether the rotation is at the right place after transforming
                assert dim[i] == new_rot[pre_computed_rotations[idx][i]]
