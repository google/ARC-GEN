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


def generate(size=None, row=None, col=None, colors=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    row: an integer with the target's row
    col: an integer with the target's column
    colors: a list of two different colors
    xpose: an integer indicating whether to transpose the grid
  """
  if size is None:
    size = common.randint(4, 12)
    row, col = common.randint(1, size - 2), common.randint(1, size - 2) 
    colors = common.random_colors(2, exclude=[common.yellow()])
    xpose = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for r in range(size):
    output[r][col] = grid[r][col] = colors[1]
  for c in range(size):
    output[row][c] = grid[row][c] = colors[0]
  for r in range(row - 1, row + 2):
    for c in range(col - 1, col + 2):
      if r == row and c == col: continue
      output[r][c] = common.yellow()
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, row=1, col=1, colors=[2, 3], xpose=0),
      generate(size=8, row=4, col=4, colors=[6, 8], xpose=1),
      generate(size=6, row=2, col=2, colors=[1, 9], xpose=1),
  ]
  test = [
      generate(size=12, row=8, col=6, colors=[5, 3], xpose=1),
  ]
  return {"train": train, "test": test}
