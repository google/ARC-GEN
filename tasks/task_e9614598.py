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


def generate(width=None, height=None, row=None, col=None, space=None,
             xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    row: a vertical coordinate where the plus should be placed
    col: a horizontal coordinate where the plus should be placed
    space: the space between the dots and the plus
    xpose: whether to transpose the grid
  """
  if width is None:
    width, height = 2 * common.randint(5, 7), 2 * common.randint(3, 7)
    space = common.randint(3, (width - 1) // 2)
    row = common.randint(2, height - 3)
    col = common.randint(space, width - space - 1)
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height)
  output[row][col - space] = grid[row][col - space] = common.blue()
  output[row][col + space] = grid[row][col + space] = common.blue()
  for dr, dc in [(1, 0), (0, 0), (-1, 0), (0, 1), (0, -1)]:
    output[row + dr][col + dc] = common.green()
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, row=4, col=4, space=3, xpose=0),
      generate(width=10, height=10, row=3, col=4, space=4, xpose=1),
  ]
  test = [
      generate(width=12, height=12, row=3, col=6, space=5, xpose=0),
      generate(width=10, height=6, row=3, col=3, space=3, xpose=1),
  ]
  return {"train": train, "test": test}
