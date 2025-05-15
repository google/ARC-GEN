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


def generate(size=None, wide=None, tall=None, col=None, row=None, color=None,
             flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    wide: the width of the colorful box
    tall: the height of the colorful box
    col: the leftmost column of the colorful box
    row: the lower offset of the colorful box
    color: a digit representing a color to be used
    flip: whether to flip the grids
    xpose: whether to transpose the grids
  """
  if size is None:
    size = common.randint(5, 10)
    wide, tall = common.randint(5, size), common.randint(3, size - 2)
    row, col = common.randint(0, 1), common.randint(0, size - wide)
    color = common.random_color()
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size)
  # Draw the colorful box.
  for r in range(size - tall, size):
    for c in range(col, col + wide):
      output[r - row][c] = grid[r - row][c] = color
  for r in range(size - tall + 1, size - 1):
    for c in range(col + 1, col + wide - 1):
      output[r - row][c] = grid[r - row][c] = common.black()
  for c in range(col + 2, col + wide - 2):
    output[size - tall - row][c] = grid[size - tall - row][c] = common.black()
  # Draw the yellow fountain.
  for r in range(size - tall + 1, size - 1):
    for c in range(col + 1, col + wide - 1):
      output[r - row][c] = common.yellow()
  for r in range(0, size - 1 - row):
    for c in range(col + 2, col + wide - 2):
      output[r][c] = common.yellow()
  for r in range(0, size - tall):
    diff = size - tall - r
    common.draw(output, r - row, col + 2 - diff, common.yellow())
    common.draw(output, r - row, col - 3 + diff + wide, common.yellow())
  # Flip and/or transpose.
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, wide=5, tall=3, col=1, row=0, color=6, flip=0, xpose=0),
      generate(size=9, wide=7, tall=5, col=2, row=0, color=7, flip=0, xpose=1),
      generate(size=6, wide=6, tall=4, col=0, row=0, color=3, flip=1, xpose=0),
  ]
  test = [
      generate(size=10, wide=9, tall=4, col=0, row=1, color=2, flip=1, xpose=1),
  ]
  return {"train": train, "test": test}
