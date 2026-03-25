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


def generate(mod=None, length=None, offset=None, rows=None, cols=None,
             wides=None, talls=None, colors=None, size=29):
  """Returns input and output grids according to the given parameters.

  Args:
    mod: how much to mod the row * col products
    length: the length of a pattern side
    offset: the offset of the rows
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    wides: a list of cutout widths
    talls: a list of cutout heights
    colors: a list of colors to use for the grid background
    size: the size of the grid
  """
  if offset is None:
    mod = common.randint(4, 9)
    length = common.randint(4, mod)
    offset = common.randint(1, length)
    wides = [common.randint(2, 5) for _ in range(5)]
    talls = [common.randint(2, 5) for _ in range(5)]
    rows = [common.randint(0, size - tall) for tall in talls]
    cols = [common.randint(0, size - wide) for wide in wides]

  grid, output = common.grids(size, size)
  for bitmap in [grid, output]:
    for col in range(size):
      for row in range(size):
        r = (offset + row) % length - length // 2
        c = (offset + col) % length - length // 2
        bitmap[row][col] = (r * r + c * c) % mod + 1
        if colors is None: continue
        r, c = row % (len(colors) // mod), col % mod
        bitmap[row][col] = colors[r * mod + c]
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(mod=6, length=6, offset=1, rows=[3, 5, 6, 7, 21],
               cols=[6, 1, 24, 4, 13], wides=[2, 4, 3, 2, 4],
               talls=[6, 3, 6, 3, 3],
               colors=[5, 4, 5, 6, 1, 2, 4, 5, 2, 1, 2, 3, 5, 6, 1, 2, 5, 4, 2,
                       1, 2, 3, 4, 5, 1, 2, 5, 4, 5, 6, 2, 3, 4, 5, 2, 1]),
      generate(mod=42, length=7, offset=5, rows=[1, 11, 11, 13, 16],
               cols=[0, 19, 19, 9, 4], wides=[4, 4, 5, 5, 3],
               talls=[4, 6, 4, 2, 6],
               colors=[5, 4, 2, 1, 2, 2, 5, 3, 2, 7, 1, 2, 3, 6, 2, 6, 2, 1, 2,
                       5, 2, 5, 5, 7, 1, 2, 2, 4, 3, 7, 2, 1, 2, 3, 3, 2, 3, 7,
                       1, 2, 5, 7, 3, 7, 1, 2, 5, 7, 5, 4, 2, 1, 2, 2, 5, 3, 2,
                       7, 1, 2, 3, 6, 2, 6, 2, 1, 2, 5, 2, 5, 5, 7, 1, 2, 2, 4,
                       3, 7, 2, 1, 2, 3, 3, 2, 2, 1, 2, 3, 3, 2, 3, 7, 1, 2, 5,
                       7, 5, 4, 2, 1, 2, 2, 5, 3, 2, 7, 1, 2, 3, 6, 2, 6, 2, 1,
                       2, 5, 2, 5, 5, 7, 1, 2, 2, 4, 3, 7, 1, 2, 2, 4, 3, 7, 2,
                       1, 2, 3, 3, 2, 3, 7, 1, 2, 5, 7, 5, 4, 2, 1, 2, 2, 5, 3,
                       2, 7, 1, 2, 3, 6, 2, 6, 2, 1, 2, 5, 2, 5, 5, 7, 2, 5, 2,
                       5, 5, 7, 1, 2, 2, 4, 3, 7, 2, 1, 2, 3, 3, 2, 3, 7, 1, 2,
                       5, 7, 5, 4, 2, 1, 2, 2, 5, 3, 2, 7, 1, 2, 3, 6, 2, 6, 2,
                       1, 3, 6, 2, 6, 2, 1, 2, 5, 2, 5, 5, 7, 1, 2, 2, 4, 3, 7,
                       2, 1, 2, 3, 3, 2, 3, 7, 1, 2, 5, 7, 5, 4, 2, 1, 2, 2, 5,
                       3, 2, 7, 1, 2, 5, 3, 2, 7, 1, 2, 3, 6, 2, 6, 2, 1, 2, 5,
                       2, 5, 5, 7, 1, 2, 2, 4, 3, 7, 2, 1, 2, 3, 3, 2, 3, 7, 1,
                       2, 5, 7, 5, 4, 2, 1, 2, 2]),
      generate(mod=8, length=4, offset=1, rows=[4, 16, 19, 19, 20],
               cols=[6, 23, 21, 24, 20], wides=[7, 4, 3, 4, 2],
               talls=[7, 3, 5, 7, 2],
               colors=[1, 2, 1, 4, 1, 6, 1, 8, 2, 1, 2, 1, 2, 1, 2, 1, 1, 4, 1,
                       6, 1, 8, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 6, 1, 8, 1, 2,
                       1, 4, 2, 1, 2, 1, 2, 1, 2, 1, 1, 8, 1, 2, 1, 4, 1, 6, 2,
                       1, 2, 1, 2, 1, 2, 1]),
  ]
  test = [
      generate(mod=18, length=9, offset=2, rows=[0, 1, 12, 12, 15],
               cols=[6, 14, 2, 13, 3], wides=[4, 3, 2, 3, 2],
               talls=[5, 7, 5, 2, 4],
               colors=[8, 1, 2, 6, 1, 2, 2, 1, 2, 3, 1, 2, 5, 1, 2, 9, 1, 2, 1,
                       8, 2, 1, 5, 9, 1, 2, 2, 1, 8, 9, 1, 5, 2, 1, 2, 9, 5, 3,
                       1, 8, 2, 1, 2, 6, 1, 5, 8, 1, 8, 9, 1, 2, 5, 1, 5, 1, 2,
                       9, 1, 2, 8, 1, 2, 6, 1, 2, 2, 1, 2, 3, 1, 2, 1, 5, 2, 1,
                       2, 9, 1, 8, 2, 1, 5, 9, 1, 2, 2, 1, 8, 9, 8, 9, 1, 2, 5,
                       1, 5, 3, 1, 8, 2, 1, 2, 6, 1, 5, 8, 1, 2, 1, 2, 3, 1, 2,
                       5, 1, 2, 9, 1, 2, 8, 1, 2, 6, 1, 2, 1, 2, 2, 1, 8, 9, 1,
                       5, 2, 1, 2, 9, 1, 8, 2, 1, 5, 9, 2, 6, 1, 5, 8, 1, 8, 9,
                       1, 2, 5, 1, 5, 3, 1, 8, 2, 1]),
  ]
  return {"train": train, "test": test}
