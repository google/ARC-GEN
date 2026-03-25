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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if width is None:
    width = common.randint(8, 24)
    height = width + common.randint(0, 4) - 2
    pixels = common.random_pixels(width, height, 0.1)
    rows, cols = zip(*pixels)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.blue()
  for r1, c1 in zip(rows, cols):
    for r2, c2 in zip(rows, cols):
      if r1 == r2:
        for c in range(min(c1, c2), max(c1, c2)):
          if output[r1][c] != common.blue(): output[r1][c] = common.cyan()
      if c1 == c2:
        for r in range(min(r1, r2), max(r1, r2)):
          if output[r][c1] != common.blue(): output[r][c1] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=10, rows=[0, 1, 4, 4, 6, 8, 9],
               cols=[3, 8, 1, 7, 1, 6, 3]),
      generate(width=11, height=10, rows=[0, 0, 2, 2, 3, 7, 7, 9],
               cols=[4, 9, 4, 8, 2, 0, 7, 6]),
      generate(width=12, height=12,
               rows=[0, 0, 2, 4, 5, 5, 6, 6, 7, 9, 9, 11, 11],
               cols=[6, 11, 10, 5, 1, 9, 6, 10, 2, 4, 8, 4, 8]),
      generate(width=9, height=8, rows=[0, 0, 2, 2, 3, 4, 5, 5, 7],
               cols=[1, 4, 4, 6, 0, 5, 2, 7, 0]),
  ]
  test = [
      generate(width=21, height=19,
               rows=[0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 14, 16, 18,
                     18],
               cols=[7, 10, 14, 2, 10, 19, 9, 1, 6, 1, 10, 11, 13, 9, 6, 14, 1,
                     1, 3]),
  ]
  return {"train": train, "test": test}
