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


def generate(rows=None, cols=None, row=None, col=None, color=None, kite=None,
             size=20):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    row: a vertical coordinates where the kite should be placed
    col: a horizontal coordinates where the kite should be placed
    color: a digit representing a color for the pixels
    kite: a digit representing a color for the kite
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.random_pixels(size, size, common.randint(2, 5) / 100)
    rows, cols = zip(*pixels)
    row, col = common.randint(1, 10), common.randint(5, size - 5 - 1)
    colors = common.random_colors(2)
    color, kite = colors[0], colors[1]

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = color
  output[row][col] = grid[row][col] = kite
  output[row + 1][col - 1] = grid[row + 1][col - 1] = kite
  output[row + 1][col] = grid[row + 1][col] = kite
  output[row + 1][col + 1] = grid[row + 1][col + 1] = kite
  output[row + 2][col - 2] = grid[row + 2][col - 2] = kite
  output[row + 2][col - 1] = grid[row + 2][col - 1] = kite
  output[row + 2][col + 1] = grid[row + 2][col + 1] = kite
  output[row + 2][col + 2] = grid[row + 2][col + 2] = kite
  output[row + 3][col - 3] = grid[row + 3][col - 3] = kite
  output[row + 3][col + 3] = grid[row + 3][col + 3] = kite
  def kite_above(r, c):
    if grid[r][c] == kite: return False  # edge case (we're inside the kite!)
    while r >= 0:
      if grid[r][c] == kite: return True
      r -= 1
    return False
  for r, c in zip(rows, cols):
    if not kite_above(r, c): continue
    r = size - 1
    while output[r][c] != kite:
      output[r][c] = color
      r -= 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 3, 4, 10, 10, 13, 18, 19],
               cols=[5, 16, 3, 1, 18, 9, 15, 1], row=5, col=9, color=8, kite=9),
      generate(rows=[1, 2, 4, 4, 9, 10, 10, 12, 14, 17, 18],
               cols=[8, 2, 13, 16, 17, 1, 9, 6, 16, 14, 1], row=5, col=7,
               color=2, kite=7),
      generate(rows=[1, 2, 2, 4, 5, 5, 7, 9, 10, 12, 12, 12, 12, 15, 16, 17, 17,
                     18, 18, 18],
               cols=[14, 5, 10, 1, 7, 18, 4, 10, 2, 0, 7, 13, 18, 4, 12, 1, 16,
                     7, 13, 19],
               row=4, col=12, color=3, kite=4),
  ]
  test = [
      generate(rows=[1, 1, 1, 2, 3, 5, 5, 7, 7, 8, 8, 10, 12, 12, 12, 14, 16,
                     16, 18, 19],
               cols=[4, 10, 18, 11, 2, 13, 18, 7, 16, 0, 4, 5, 1, 11, 16, 18,
                     7, 14, 17, 10],
               row=3, col=6, color=6, kite=1),
  ]
  return {"train": train, "test": test}
