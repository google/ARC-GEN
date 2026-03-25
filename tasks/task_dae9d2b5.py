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


def generate(rows=None, cols=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a digit representing different colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols, colors = [], [], []
    for color in [4, 3]:
      while True:
        pixels = common.random_pixels(size, size)
        if pixels: break
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      colors.extend([color] * len(pixels))

  grid, output = common.grid(2 * size, size), common.grid(size, size)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c if color == 4 else c + size] = color
    output[r][c] = common.pink()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 0, 0, 1, 2], cols=[0, 1, 0, 0, 1, 0, 2],
               colors=[4, 4, 4, 3, 3, 3, 3]),
      generate(rows=[0, 0, 1, 2, 0, 0, 1, 2], cols=[0, 2, 0, 2, 0, 1, 0, 0],
               colors=[4, 4, 4, 4, 3, 3, 3, 3]),
      generate(rows=[0, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[2, 1, 2, 0, 1, 1, 0, 2, 2],
               colors=[4, 4, 4, 4, 4, 3, 3, 3, 3]),
      generate(rows=[0, 0, 2, 0, 1], cols=[0, 1, 0, 0, 2],
               colors=[4, 4, 4, 3, 3]),
      generate(rows=[1, 2, 0, 2, 2], cols=[0, 2, 1, 0, 1],
               colors=[4, 4, 3, 3, 3]),
  ]
  test = [
      generate(rows=[0, 0, 1, 2, 0, 1, 1, 2], cols=[1, 2, 0, 1, 0, 0, 1, 0],
               colors=[4, 4, 4, 4, 3, 3, 3, 3]),
      generate(rows=[0, 1, 2, 0, 1, 1, 1, 2], cols=[2, 1, 0, 1, 0, 1, 2, 0],
               colors=[4, 4, 4, 3, 3, 3, 3, 3]),
  ]
  return {"train": train, "test": test}
