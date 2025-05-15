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


def generate(width=None, height=None, row=None, col=None, thicks=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    row: a vertical coordinates where the square should be placed
    col: a horizontal coordinates where the square should be placed
    thicks: how thick the creme and the cookie should be
    colors: the colors of the creme and the cookie
  """
  if width is None:
    width, height = common.randint(10, 15), common.randint(10, 15)
    thicks = [common.randint(1, 2) for _ in range(2)]
    size = thicks[0] + 2 * thicks[1]
    row = common.randint(1, height - size - 1)
    col = common.randint(1, width - size - 1)
    colors = common.random_colors(2)

  size = thicks[0] + 2 * thicks[1]
  grid, output = common.grid(width, height), common.grid(size, size)
  for r in range(size):
    for c in range(size):
      grid[row + r][col + c] = colors[1]
      output[r][c] = colors[0]
  for r in range(thicks[0]):
    for c in range(thicks[0]):
      grid[row + r + thicks[1]][col + c + thicks[1]] = colors[0]
      output[r + thicks[1]][c + thicks[1]] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=12, row=1, col=3, thicks=[2, 1], colors=[4, 2]),
      generate(width=11, height=12, row=2, col=4, thicks=[1, 1], colors=[3, 1]),
      generate(width=13, height=12, row=6, col=2, thicks=[1, 2], colors=[6, 4]),
  ]
  test = [
      generate(width=13, height=14, row=1, col=2, thicks=[2, 2], colors=[8, 3]),
  ]
  return {"train": train, "test": test}
