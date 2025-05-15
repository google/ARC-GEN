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


def generate(mod=None, modset=None, rows=None, cols=None, wides=None,
             talls=None, size=21):
  """Returns input and output grids according to the given parameters.

  Args:
    mod: how much to mod the row * col products
    modset: how much to offset the indices before taking the mod
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    wides: a list of cutout widths
    talls: a list of cutout heights
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    for r in range(size):
      for c in range(size):
        color = (r + 2) // (c + 2) if r > c else (c + 2) // (r + 2)
        color = color if r != c else 2  # Special case for the diagonal.
        grid[r][c] = output[r][c] = (color + modset) % mod + 1
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          grid[r][c] = common.black()
    for c in range(size):
      for r in range(c):
        if grid[r][c] == 0 and grid[c][r] == 0: return False
    return True

  if mod is None:
    mod, modset = common.randint(5, 9), common.randint(1, 4)
    while True:
      wides = [common.randint(2, 5) for _ in range(5)]
      talls = [common.randint(2, 5) for _ in range(5)]
      rows = [common.randint(0, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(mod=6, modset=4, rows=[4, 7, 11, 11, 18],
               cols=[11, 8, 10, 12, 10], wides=[3, 3, 2, 5, 4],
               talls=[2, 3, 2, 4, 2]),
      generate(mod=7, modset=3, rows=[3, 6, 8, 14, 17], cols=[3, 9, 12, 2, 8],
               wides=[3, 3, 5, 4, 4], talls=[5, 3, 2, 2, 2]),
      generate(mod=8, modset=2, rows=[2, 10, 13, 14], cols=[16, 11, 10, 9],
               wides=[2, 2, 5, 3], talls=[5, 3, 3, 5]),
  ]
  test = [
      generate(mod=9, modset=1, rows=[1, 8, 15, 15, 18],
               cols=[10, 0, 4, 15, 12], wides=[2, 5, 5, 5, 5],
               talls=[5, 2, 3, 2, 2]),
  ]
  return {"train": train, "test": test}
