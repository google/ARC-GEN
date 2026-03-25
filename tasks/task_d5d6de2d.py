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


def generate(size=None, rows=None, cols=None, wides=None, talls=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
  """
  if size is None:
    mult = common.randint(2, 5)
    size = 5 * mult
    num_boxes = common.randint(mult - 1, mult)
    while True:
      wides = [common.randint(2, 9) for _ in range(num_boxes)]
      talls = [common.randint(2, 9) for _ in range(num_boxes)]
      rows = [common.randint(0, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break

  grid, output = common.grids(size, size)
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.red()
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        grid[r][c] = common.black()
        output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[1, 5], cols=[1, 4], wides=[3, 4], talls=[3, 5]),
      generate(size=10, rows=[1], cols=[4], wides=[3], talls=[4]),
      generate(size=15, rows=[1, 7], cols=[1, 10], wides=[5, 2], talls=[5, 2]),
  ]
  test = [
      generate(size=10, rows=[0, 4], cols=[0, 1], wides=[3, 8], talls=[3, 6]),
      generate(size=25, rows=[1, 7, 9, 18], cols=[1, 4, 15, 1],
               wides=[7, 2, 9, 5], talls=[3, 2, 4, 6]),
  ]
  return {"train": train, "test": test}
