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


def generate(width=None, height=None, brow=None, bcol=None, prows=None,
             pcols=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brow: The row of the pink box.
    bcol: The column of the pink box.
    prows: The rows of the black pixels.
    pcols: The cols of the black pixels.
    xpose: Whether to transpose the grids.
  """

  if width is None:
    pillars = common.randint(4, 8)
    width, height = 3 * pillars + 1, common.randint(10, 20)
    brow = common.randint(4, height - 6)
    bcol = 3 * common.randint(1, pillars - 2) + 1
    prows, pcols = [], []
    for row in range(height):
      for col in range(width):
        if common.randint(0, 9): continue
        prows.append(row)
        pcols.append(col)
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height, 8)
  common.hollow_rect(grid, width, height, 0, 0, 0)
  common.hollow_rect(output, width, height, 0, 0, 0)
  # Draw the vertical black stripes.
  for col in range(0, width, 3):
    for row in range(height):
      output[row][col] = grid[row][col] = 0
  # Draw the black pixels.
  for prow, pcol in zip(prows, pcols):
    output[prow][pcol] = grid[prow][pcol] = 0
  # Draw the pink box.
  common.rect(grid, 2, 2, brow, bcol, 6)
  common.rect(output, 2, 2, brow, bcol, 6)
  # Draw the upper yellow boxes.
  left, rite = bcol - 3, bcol + 5
  for row in range(brow - 2, -2, -2):
    for col in range(left, rite):
      if col in [bcol, bcol + 1]: continue
      for r in range(row, row + 2):
        if common.get_pixel(output, r, col) == 8: common.draw(output, r, col, 4)
    left, rite = left - 3, rite + 3
  # Draw the lower yellow boxes.
  left, rite = bcol - 3, bcol + 5
  for row in range(brow + 2, height + 2, 2):
    for col in range(left, rite):
      if col in [bcol, bcol + 1]: continue
      for r in range(row, row + 2):
        if common.get_pixel(output, r, col) == 8: common.draw(output, r, col, 4)
    left, rite = left - 3, rite + 3
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=14, brow=6, bcol=7,
               prows=[1, 2, 5, 5, 7, 10, 10, 11, 12],
               pcols=[4, 2, 11, 13, 14, 4, 5, 7, 8], xpose=True),
      generate(width=19, height=12, brow=5, bcol=7,
               prows=[2, 2, 3, 3, 4, 5, 5, 5, 5, 8, 8, 9, 9, 10],
               pcols=[5, 10, 7, 16, 11, 1, 2, 14, 17, 13, 16, 14, 17, 8],
               xpose=False),
      generate(width=22, height=16, brow=5, bcol=10,
               prows=[4, 5, 7, 8, 9, 10, 13, 13, 14, 14, 14],
               pcols=[11, 4, 13, 17, 5, 11, 8, 17, 5, 11, 13], xpose=False),
  ]
  test = [
      generate(width=25, height=20, brow=9, bcol=10,
               prows=[1, 4, 4, 5, 6, 6, 6, 7, 7, 8, 8, 10, 11, 11, 11, 11, 12, 14, 15, 15, 16, 16, 16, 17, 17, 17, 18],
               pcols=[22, 17, 8, 4, 10, 5, 1, 17, 13, 17, 13, 8, 1, 4, 10, 17, 11, 19, 13, 23, 13, 10, 1, 10, 16, 17, 14],
               xpose=True),
  ]
  return {"train": train, "test": test}
