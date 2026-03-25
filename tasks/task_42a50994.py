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


def generate(width=None, height=None, rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
  """
  if width is None:
    width, height = common.randint(5, 20), common.randint(5, 20)
    rows, cols = [], []
    for r in range(height):
      for c in range(width):
        if common.randint(0, 9) != 0: continue
        rows.append(r)
        cols.append(c)
    color = common.random_color()

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = color
  def get_val(r, c):
    if r < 0 or r >= height or c < 0 or c >= width: return 0
    return 1 if output[r][c] > 0 else 0
  for r in range(height):
    for c in range(width):
      friends = 0
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          friends += get_val(r + dr, c + dc)
      if friends > 1: continue
      output[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=16,
               rows=[0, 1, 2, 2, 2, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9,
                     10, 10, 12, 13, 13, 14, 15],
               cols=[1, 0, 4, 7, 9, 4, 2, 3, 3, 8, 2, 6, 5, 10, 5, 6,
                     1, 4, 1, 6, 9, 4, 8],
               color=8),
      generate(width=18, height=12,
               rows=[0, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5,
                     6, 6, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 11],
               cols=[11, 1, 5, 8, 10, 14, 2, 14, 1, 9, 11, 14, 17, 7,
                     8, 14, 2, 12, 5, 7, 8, 2, 11, 13, 7, 11, 2, 16,
                     17],
               color=6),
      generate(width=19, height=11,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                     4, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 8, 9,
                     9, 9, 9, 9, 10, 10, 10, 10],
               cols=[12, 15, 4, 9, 7, 10, 16, 9, 11, 12, 16, 1, 4, 6,
                     13, 15, 16, 2, 8, 2, 12, 14, 15, 3, 17, 18, 0,
                     3, 11, 13, 16, 0, 9, 11, 16, 17, 1, 10, 13, 18],
               color=5),
      generate(width=9, height=17,
               rows=[0, 0, 1, 2, 2, 3, 3, 4, 5, 5, 5, 5, 6, 6, 8, 8,
                     9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 13, 14,
                     14, 15, 15, 15, 15, 15, 16],
               cols=[5, 7, 4, 1, 6, 3, 4, 2, 2, 4, 7, 8, 0, 2, 2, 6,
                     2, 1, 6, 8, 0, 2, 4, 7, 1, 7, 5, 4, 5, 0, 2, 4,
                     7, 8, 2],
               color=4),
  ]
  test = [
      generate(width=14, height=17,
               rows=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3,
                     3, 4, 4, 4, 4, 5, 6, 6, 7, 7, 7, 8, 8, 9, 9, 10,
                     10, 10, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13,
                     13, 14, 14, 14, 14, 15, 15, 16, 16, 16, 16, 16],
               cols=[1, 4, 10, 13, 0, 7, 8, 9, 10, 13, 0, 6, 2, 4, 9,
                     10, 11, 0, 2, 10, 13, 5, 0, 11, 4, 5, 8, 10, 11,
                     1, 13, 4, 6, 10, 3, 5, 3, 4, 5, 7, 8, 0, 3, 6,
                     12, 0, 2, 8, 11, 0, 5, 2, 3, 6, 12, 13],
               color=3),
  ]
  return {"train": train, "test": test}
