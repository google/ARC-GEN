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


def generate(rows=None, cols=None, colors=None, size=4):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the color to be used
    size: the width and height of the (square) grid
    b: the integer used for all background cells
    y: the integer used for all "yellow" cells
    g: the integer used for all "green" cells
  """
  if rows is None:
    rows, cols, colors = [], [], []
    for color in [1, 2]:
      pixels = common.random_pixels(size, size)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      colors.extend([color] * len(pixels))

  grid, output = common.grid(size, 2 * size + 1), common.grid(size, size)
  for c in range(size):
    grid[size][c] = common.yellow()
  for r, c, color in zip(rows, cols, colors):
    grid[r if color == 1 else size + r + 1][c] = color
    output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 3, 3, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3],
               cols=[0, 1, 1, 3, 1, 0, 2, 0, 1, 2, 3, 2, 3, 0, 1, 2, 3],
               colors=[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 0, 1, 2, 2, 2, 2, 3, 3, 3],
               cols=[0, 1, 2, 1, 3, 2, 3, 0, 1, 3, 3, 3, 0, 1, 2, 3, 0, 1, 3],
               colors=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       2, 2, 2, 2, 2, 2, 2, 2, 2]),
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 0, 0, 0, 1, 2, 3, 3],
               cols=[0, 1, 0, 2, 0, 1, 3, 0, 1, 2, 3, 0, 1, 3, 2, 1, 0, 2],
               colors=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]),
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 0, 0, 1, 2, 2, 3],
               cols=[0, 2, 0, 1, 3, 0, 2, 3, 1, 3, 0, 1, 2, 0, 1, 2],
               colors=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 3, 3, 0, 0, 1, 2, 2, 3, 3, 3],
               cols=[0, 2, 0, 2, 1, 0, 2, 0, 1, 2, 1, 3, 0, 1, 2],
               colors=[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
