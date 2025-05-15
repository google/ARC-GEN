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


def generate(
    width=None,
    height=None,
    rows=None,
    cols=None,
    brows=None,
    bcols=None,
    wides=None,
    talls=None,
    color=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of boxes
    talls: a list of heights of boxes
    color: a digit representing a color to be used
  """
  if width is None:
    wides = [common.randint(8, 11), common.randint(3, 4)]
    talls = [common.randint(8, 11), common.randint(3, 4)]
    width = wides[0] + common.randint(3, 5)
    height = talls[0] + common.randint(3, 5)
    brows = [common.randint(1, height - talls[0] - 1)]
    bcols = [common.randint(1, width - wides[0] - 1)]
    brows += [common.randint(brows[0] + 2, brows[0] + talls[0] - talls[1] - 2)]
    bcols += [common.randint(bcols[0] + 2, bcols[0] + wides[0] - wides[1] - 2)]
    rows, cols = [], []
    rows += [brows[0] - 1, brows[0] + talls[0]]
    rows += [common.randint(brows[0], brows[0] + talls[0] - 1) for _ in brows]
    cols += [common.randint(bcols[0], bcols[0] + wides[0] - 1) for _ in bcols]
    cols += [bcols[0] - 1, bcols[0] + wides[0]]
    color = common.random_color(exclude=[common.gray()])

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.gray()
  for i in range(len(brows)):
    boxrow, boxcol, wide, tall = brows[i], bcols[i], wides[i], talls[i]
    for r in range(boxrow, boxrow + tall):
      output[r][boxcol + wide - 1] = output[r][boxcol] = color
      if not i: continue
      grid[r][boxcol + wide - 1] = grid[r][boxcol] = color
    for c in range(boxcol, boxcol + wide):
      output[boxrow + tall - 1][c] = output[boxrow][c] = color
      if not i: continue
      grid[boxrow + tall - 1][c] = grid[boxrow][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=12, rows=[1, 6, 6, 11], cols=[4, 1, 11, 4],
               brows=[2, 4], bcols=[2, 5], wides=[9, 3], talls=[9, 4], color=1),
      generate(width=13, height=15, rows=[1, 5, 8, 12], cols=[5, 1, 10, 5],
               brows=[2, 5], bcols=[2, 4], wides=[8, 3], talls=[10, 3],
               color=3),
      generate(width=14, height=15, rows=[2, 6, 8, 13], cols=[6, 12, 1, 7],
               brows=[3, 5], bcols=[2, 4], wides=[10, 4], talls=[10, 4],
               color=4),
  ]
  test = [
      generate(width=15, height=15, rows=[1, 6, 9, 13], cols=[7, 2, 12, 5],
               brows=[2, 5], bcols=[3, 5], wides=[9, 4], talls=[11, 3],
               color=8),
  ]
  return {"train": train, "test": test}
