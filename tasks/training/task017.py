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
             wides=None, talls=None, size=21):
  """Returns input and output grids according to the given parameters.

  Args:
    mod: how much to mod the row * col products
    length: the length of a pattern side
    offset: the offset of the rows
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    wides: a list of cutout widths
    talls: a list of cutout heights
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
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(mod=6, length=6, offset=1, rows=[4, 5, 6, 11, 16],
               cols=[15, 8, 7, 3, 4], wides=[5, 2, 4, 2, 3],
               talls=[3, 5, 3, 3, 3]),
      generate(mod=7, length=7, offset=5, rows=[3, 3, 6, 8, 13],
               cols=[4, 16, 17, 0, 16], wides=[5, 2, 3, 5, 2],
               talls=[4, 4, 4, 3, 3]),
      generate(mod=8, length=4, offset=1, rows=[2, 4, 5, 5, 14],
               cols=[0, 14, 9, 4, 1], wides=[5, 3, 3, 4, 5],
               talls=[2, 2, 4, 5, 5]),
  ]
  test = [
      generate(mod=9, length=9, offset=2, rows=[1, 8, 12, 15, 15],
               cols=[9, 4, 14, 0, 4], wides=[5, 4, 2, 2, 3],
               talls=[3, 3, 4, 2, 5]),
  ]
  return {"train": train, "test": test}
