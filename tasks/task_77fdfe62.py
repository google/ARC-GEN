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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of four digits representing the colors to be used
  """
  if rows is None:
    size = 2 * common.randint(1, 3)
    while True:
      pixels = common.random_pixels(size, size)
      if pixels: break
    rows, cols = zip(*pixels)
    colors = common.random_colors(4, exclude=[common.blue(), common.cyan()])

  grid, output = common.grid(size + 4, size + 4), common.grid(size, size)
  for i in range(4 + size):
    for r, c in [(1, i), (i, 1), (size + 2, i), (i, size + 2)]:
      grid[r][c] = common.blue()
  grid[0][0] = colors[0]
  grid[0][size + 3] = colors[1]
  grid[size + 3][0] = colors[2]
  grid[size + 3][size + 3] = colors[3]
  for r, c in zip(rows, cols):
    grid[r + 2][c + 2] = common.cyan()
    if r < size // 2 and c < size // 2:
      color = colors[0]
    elif r < size // 2 and c >= size // 2:
      color = colors[1]
    elif r >= size // 2 and c < size // 2:
      color = colors[2]
    else:
      color = colors[3]
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, rows=[0, 1, 1, 1, 2, 3, 3, 3],
               cols=[1, 0, 1, 3, 2, 0, 2, 3], colors=[2, 3, 4, 6]),
      generate(size=2, rows=[0, 0, 1], cols=[0, 1, 0], colors=[9, 4, 2, 3]),
      generate(size=4, rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
               cols=[1, 3, 0, 1, 2, 0, 2, 3, 0, 1, 2], colors=[6, 2, 7, 4]),
  ]
  test = [
      generate(size=6,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5],
               cols=[1, 2, 0, 1, 2, 4, 2, 4, 1, 3, 4, 0, 1, 3, 5, 1, 4],
               colors=[3, 4, 7, 5]),
  ]
  return {"train": train, "test": test}
