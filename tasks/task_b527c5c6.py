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


def generate(size=None, rows=None, cols=None, wides=None, talls=None,
             dotrow=None, dotcol=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    dotrow: the vertical coordinate of the dot
    dotcol: the horizontal coordinate of the dot
    flip: a boolean indicating whether the grids should be flipped
    xpose: a boolean indicating whether the grids should be transposed
  """
  if size is None:
    size = 10 * (2 if common.randint(0, 3) else 1)
    # Choose widths -- make sure they're wide (or tall) enough for the beam.
    if size == 10:
      wides, talls = [2, common.randint(4, 6)], [common.randint(4, 6), 2]
    else:
      wide0, tall1 = common.randint(2, 5), common.randint(2, 6)
      tall0, wide1 = common.randint(10, 18), common.randint(9, 13)
      wides = [wide0, max(wide1, 2 * tall1 + 1)]
      talls = [max(tall0, 2 * wide0 + 1), tall1]
    # Choose positions -- we assume box 0 is to the left of box 1.
    spacing = common.randint(1, size - sum(wides) - 1)
    rows = [common.randint(1, size - tall) for tall in talls]
    cols = [common.randint(1, size - sum(wides) - spacing)]
    cols.append(cols[0] + wides[0] + spacing)
    # Choose locations of the dots.
    dotrow = common.randint(wides[0], talls[0] - wides[0])
    dotcol = common.randint(talls[1], wides[1] - talls[1])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size)
  defect = rows[1] + talls[1] < rows[0] + dotrow - wides[0]  # Aims at partner!
  for idx in range(len(rows)):
    row, col, wide, tall = rows[idx], cols[idx], wides[idx], talls[idx]
    for r in range(tall):
      for c in range(wide):
        output[row + r][col + c] = grid[row + r][col + c] = common.green()
    r, c = row + dotrow * (1 - idx), col + dotcol * idx
    if defect and not idx: c += wides[0] - 1
    output[r][c] = grid[r][c] = common.red()
  locol = 0 if not defect else cols[0] + wides[0]
  hicol = cols[0] if not defect else size
  for c in range(locol, hicol):
    r = rows[0] + dotrow
    for dr in range(-wides[0] + 1, wides[0]):
      output[r + dr][c] = common.green()
    output[r][c] = common.red()
  for r in range(0, rows[1]):
    c = cols[1] + dotcol
    for dc in range(-talls[1] + 1, talls[1]):
      output[r][c + dc] = common.green()
    output[r][c] = common.red()
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[2, 4], cols=[3, 6], wides=[2, 4], talls=[6, 2],
               dotrow=3, dotcol=2, flip=1, xpose=0),
      generate(size=20, rows=[1, 10], cols=[4, 10], wides=[2, 10],
               talls=[18, 3], dotrow=4, dotcol=5, flip=1, xpose=1),
      generate(size=20, rows=[0, 10], cols=[3, 9], wides=[3, 11],
               talls=[14, 5], dotrow=5, dotcol=5, flip=0, xpose=1),
      generate(size=20, rows=[5, 4], cols=[0, 6], wides=[5, 11],
               talls=[15, 4], dotrow=10, dotcol=6, flip=1, xpose=1),
  ]
  test = [
      generate(size=20, rows=[0, 14], cols=[4, 7], wides=[3, 13],
               talls=[11, 6], dotrow=5, dotcol=6, flip=0, xpose=0),
  ]
  return {"train": train, "test": test}
