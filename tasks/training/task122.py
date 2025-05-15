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


def generate(width=None, height=None, row=None, col=None, idx=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    row: a vertical coordinate where pixels should start
    col: a horizontal coordinates where pixels should start
    idx: the index of the pixel to be incremented
    xpose: whether to transpose the grid
  """
  if width is None:
    width = common.randint(7, 21)
    height = common.randint(7, width)
    row, col = common.randint(1, height - 2), common.randint(0, 1)
    idx = common.randint(1 - col, (width + 1 - col) // 2 - 3)
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height)
  for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
      grid[row + dr][col + 2 * idx + dc] = common.red()
      output[row + dr][col + 2 * (idx + 1) + dc] = common.red()
  for c in range(col, width, 2):
    grid[row][c] = output[row][c] = common.green()
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=7, row=3, col=1, idx=0, xpose=0),
      generate(width=13, height=7, row=4, col=0, idx=2, xpose=1),
      generate(width=7, height=7, row=2, col=0, idx=1, xpose=1),
  ]
  test = [
      generate(width=17, height=7, row=4, col=0, idx=4, xpose=0),
  ]
  return {"train": train, "test": test}
