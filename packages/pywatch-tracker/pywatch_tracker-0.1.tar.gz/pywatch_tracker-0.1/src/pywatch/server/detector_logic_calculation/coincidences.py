import typing
from collections import defaultdict

from .detector import *
from .vector import *
import random


class Coincidences(defaultdict):
    def __init__(self):
        super().__init__(list)

    def __getitem__(self, item: typing.List[int]) -> typing.List[typing.Tuple[Vector, Vector]]:
        item.sort()

        return super().__getitem__(str(item).replace(" ", ""))

    def to_dict(self, mode: typing.Literal["mean", "random"] = "mean") -> typing.Dict[
        int, typing.Tuple[Vector, Vector]]:
        dct = dict()

        # TODO include random selection
        for key, item in self.items():
            start_points = [start for start, _ in item]
            directions = [dir_ for _, dir_ in item]

            if mode == "mean":
                start_point_mean = sum(start_points, start=Vector()) / len(start_points)
                direction_mean = sum(directions, start=Vector()) / len(directions)

                dct[key] = (start_point_mean, direction_mean / direction_mean.norm())
            elif mode == "random":
                dct[key] = random.choice(item)

        return dct


def get_course_coincidences(detectors: list[Detector]) -> typing.List[typing.List[int]]:
    n = len(detectors)
    coincidences = []

    for i in range(n):
        for j in range(n):
            if j == i:
                continue

            coincidence_indices = [i, j]
            for k in range(n):
                if k == j or k == i:
                    continue

                # if vectors_on_line(x=detectors[i].position, y=detectors[j].position, z=detectors[k].position,
                #                    radius=2.5):
                #     coincidence_indices.append(k)
                v1 = detectors[i].position
                v2 = detectors[j].position
                v3 = detectors[k].position
                if line_in_cuboid(v1, v2, v3, DETECTOR_WIDTH * 1.5, DETECTOR_HEIGHT):
                    coincidence_indices.append(k)

            coincidences.append(coincidence_indices)

    return coincidences


def calculate_coincidences(detectors: typing.List[Detector]) -> Coincidences:
    coincidences = Coincidences()
    cc = get_course_coincidences(detectors)

    for coin in cc:
        i1, i2 = coin[0:2]
        for s1 in detectors[i1].sections:
            for s2 in detectors[i2].sections:
                indices = [i1, i2]
                line = Line(s1, s2)
                # indices.extend([i for i in coin[2:] if is_on_line(line, detectors[i])])
                indices.extend([i for i in coin[2:] if detectors[i].line_in_detector(line)])

                coincidences[indices].append((line.position, line.direction))

    return coincidences
