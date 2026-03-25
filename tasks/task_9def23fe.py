# Copyright 2026 Google LLC
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


def generate(width=None, height=None, length=None, brow=None, bcol=None,
             color=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the box.
    brow: The row of the box.
    bcol: The column of the box.
    color: The color of the pixels.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
  """

  if width is None:
    width, height = common.randint(15, 25), common.randint(15, 25)
    length, color = common.randint(5, 8), common.random_color(exclude=[2])
    brow = common.randint(1, height - length - 1)
    bcol = common.randint(1, width - length - 1)
    while True:
      prows, pcols = [], []
      for i in range(length):
        if 1 <= brow - 2 and common.randint(0, 1):
          prows.append(common.randint(1, brow - 2))
          pcols.append(bcol + i)
        if brow + length + 1 <= height - 2 and common.randint(0, 1):
          prows.append(common.randint(brow + length + 1, height - 2))
          pcols.append(bcol + i)
        if 1 <= bcol - 2 and common.randint(0, 1):
          prows.append(brow + i)
          pcols.append(common.randint(1, bcol - 2))
        if bcol + length + 1 <= width - 2 and common.randint(0, 1):
          prows.append(brow + i)
          pcols.append(common.randint(bcol + length + 1, width - 2))
      if prows: break

  grid, output = common.grids(width, height)
  common.rect(grid, length, length, brow, bcol, 2)
  common.rect(output, length, length, brow, bcol, 2)
  for prow, pcol in zip(prows, pcols):
    output[prow][pcol] = grid[prow][pcol] = color
  for i in range(length):
    if not sum(grid[r][bcol + i] for r in range(brow)):
      for r in range(brow):
        output[r][bcol + i] = 2
    if not sum(grid[r][bcol + i] for r in range(brow + length, height)):
      for r in range(brow + length, height):
        output[r][bcol + i] = 2
    if not sum(grid[brow + i][c] for c in range(bcol)):
      for c in range(bcol):
        output[brow + i][c] = 2
    if not sum(grid[brow + i][c] for c in range(bcol + length, width)):
      for c in range(bcol + length, width):
        output[brow + i][c] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=20, length=5, brow=5, bcol=4, color=3,
               prows=[1, 1, 3, 5, 7, 8, 13, 16],
               pcols=[4, 8, 6, 12, 1, 13, 8, 5]),
      generate(width=25, height=21, length=8, brow=1, bcol=2, color=8,
               prows=[1, 2, 4, 7, 12, 13, 15, 17],
               pcols=[21, 19, 15, 18, 3, 9, 5, 8]),
      generate(width=17, height=20, length=6, brow=4, bcol=5, color=4,
               prows=[1, 1, 4, 7, 8, 9, 13, 14],
               pcols=[6, 10, 2, 1, 2, 14, 5, 9]),
  ]
  test = [
      generate(width=20, height=20, length=7, brow=2, bcol=9, color=1,
               prows=[2, 3, 4, 7, 8, 12, 17, 19],
               pcols=[6, 19, 5, 1, 19, 9, 13, 15]),
  ]
  return {"train": train, "test": test}
