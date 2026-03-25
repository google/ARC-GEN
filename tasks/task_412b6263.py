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


def generate(width=None, height=None, wide=None, tall=None, row=None, col=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The width of the box.
    tall: The height of the box.
    row: The row of the pixel.
    col: The column of the pixel.
  """

  if width is None:
    width, height = common.randint(5, 10), common.randint(6, 10)
    wide = common.randint(2, (width - 1) // 2)
    tall = common.randint(2, height - 1)
    row, col = common.randint(0, tall - 1), common.randint(0, wide - 1)

  grid = common.grid(width, height, 7)
  common.rect(grid, wide, tall, 0, 0, 5)
  common.rect(grid, wide, tall, height - tall, width - wide, 5)
  grid[row][col] = 9
  grid[height - tall + row][width - wide + col] = 9
  creme = common.transpose(common.flop(grid))
  creme = [[1] + row + [1] for row in creme]
  output = []
  output.extend([[7] + [1] * height + [7]])
  output.extend(creme)
  output.extend([[7] + [1] * height + [7]])
  output.extend(creme)
  output.extend([[7] + [1] * height + [7]])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=9, wide=2, tall=4, row=2, col=1),
      generate(width=8, height=7, wide=3, tall=3, row=2, col=0),
      generate(width=5, height=5, wide=2, tall=2, row=0, col=1),
  ]
  test = [
      generate(width=10, height=5, wide=4, tall=4, row=3, col=0),
  ]
  return {"train": train, "test": test}
