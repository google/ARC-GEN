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


def generate(rows=None, cols=None, groups=None, colors=None, flip=None,
             xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    groups: The groups of the pixels.
    colors: The colors of the groups.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  if rows is None:
    colors = common.random_colors(3, exclude=[1, 4])
    rows, cols, groups = [], [], []
    for group in range(3):
      r, c = common.conway_sprite(3, 3)
      rows.extend(r)
      cols.extend(c)
      groups.extend([group] * len(r))
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(11, 7)
  for col in range(11):
    output[3][col] = grid[3][col] = 4
  for row in range(7):
    for col in [3, 7]:
      output[row][col] = grid[row][col] = 4
  for group in range(3):
    output[1][4 * group + 1] = grid[1][4 * group + 1] = colors[group]
  for row, col, group in zip(rows, cols, groups):
    grid[row + 4][4 * group + col] = 1
    output[row + 4][4 * group + col] = colors[group]
  if flip: grid, output = common.flip(grid), common.flip(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 1, 0, 2, 0, 1, 2, 2, 0, 2, 0, 1, 1, 2], groups=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], colors=[7, 3, 8], flip=False, xpose=True),
      generate(rows=[0, 1, 2, 2, 2, 0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2], cols=[0, 1, 0, 1, 2, 1, 0, 1, 2, 0, 2, 0, 2, 0, 2, 1], groups=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2], colors=[3, 2, 6], flip=False, xpose=False),
  ]
  test = [
      generate(rows=[1, 1, 2, 2, 0, 0, 1, 2, 0, 1, 1, 1, 2, 2], cols=[1, 2, 0, 2, 0, 1, 1, 2, 2, 0, 1, 2, 0, 2], groups=[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], colors=[6, 2, 8], flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
