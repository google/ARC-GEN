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


def generate(width=None, height=None, row=None, col=None, color=None, flip=None,
             flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    row: The row of the box.
    col: The column of the box.
    color: The color of the box.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
  """

  if width is None:
    width, height = 2 * common.randint(2, 5), 2 * common.randint(2, 5)
    row = common.randint(0, height // 2 - 1)
    col = common.randint(0, width // 2 - 1)
    color = common.random_color(exclude=[8])
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height, 8)
  grid[row][col] = color
  for r in range(row + 1):
    for c in range(col + 1):
      output[r][c] = color
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=6, row=2, col=2, color=4, flip=True, flop=False),
      generate(width=6, height=6, row=2, col=1, color=9, flip=False, flop=True),
      generate(width=8, height=10, row=4, col=2, color=6, flip=False, flop=False),
      generate(width=4, height=4, row=0, col=1, color=6, flip=False, flop=True),
  ]
  test = [
      generate(width=10, height=10, row=2, col=1, color=4, flip=True, flop=True),
  ]
  return {"train": train, "test": test}
