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


def generate(rows=None, cols=None, wides=None, talls=None, xpose=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of widths of the pixels to be placed
    talls: a list of heights of the pixels to be placed
    xpose: a list of x-positions of the pixels to be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    while True:
      wides = [common.randint(3, 6) for _ in range(2)]
      if sum(wides) in [8, 9]: break
    talls = [common.randint(3, 6) for _ in range(2)]
    rows = [common.randint(0, size - tall) for tall in talls]
    cols = [9 - sum(wides), size - wides[1]]
    xpose = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.gray()
        output[r][c] = common.red()
        if r in [row, row + tall - 1] or c in [col, col + wide - 1]:
          output[r][c] = common.yellow()
        if r in [row, row + tall - 1] and c in [col, col + wide - 1]:
          output[r][c] = common.blue()
  if xpose:
    grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 5], cols=[1, 6], wides=[4, 4], talls=[4, 5], xpose=0),
      generate(rows=[0, 4], cols=[0, 6], wides=[5, 4], talls=[6, 6], xpose=1),
  ]
  test = [
      generate(rows=[1, 4], cols=[0, 7], wides=[6, 3], talls=[4, 6], xpose=1),
  ]
  return {"train": train, "test": test}
