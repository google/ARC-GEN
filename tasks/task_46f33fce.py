# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(rows=None, cols=None, colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) input grid
  """
  if rows is None:
    half = size // 2
    pixels = common.sample(common.all_pixels(half, half), common.randint(5, 6))
    rows, cols = zip(*pixels)
    colors = [common.random_color() for _ in range(len(pixels))]

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for r, c, color in zip(rows, cols, colors):
    grid[2 * r + 1][2 * c + 1] = color
    for dr in range(4):
      for dc in range(4):
        output[4 * r + dr][4 * c + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2, 3, 4], cols=[0, 0, 1, 2, 3, 4],
               colors=[2, 4, 1, 3, 4, 3]),
      generate(rows=[0, 0, 1, 3, 4, 4], cols=[0, 1, 1, 4, 3, 4],
               colors=[1, 3, 4, 8, 2, 2]),
      generate(rows=[0, 0, 4, 4, 4], cols=[0, 1, 0, 1, 4],
               colors=[3, 2, 1, 1, 4]),
  ]
  test = [
      generate(rows=[1, 2, 3, 3, 4], cols=[1, 2, 1, 3, 0],
               colors=[6, 1, 3, 4, 2]),
  ]
  return {"train": train, "test": test}
