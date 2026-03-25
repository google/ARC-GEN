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


def generate(colors=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  if colors is None:
    colors = common.random_colors(2, exclude=[5])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(10, 10)
  for i in range(2, 8):
    output[2][i] = grid[2][i] = 5
    output[7][i] = grid[7][i] = 5
    output[i][2] = grid[i][2] = 5
    output[i][7] = grid[i][7] = 5
  output[1][1] = grid[1][1] = colors[0]
  output[1][8] = grid[1][8] = colors[1]
  for r, c in [(3, 3), (3, 4), (4, 3), (4, 4), (5, 5), (5, 6), (6, 5), (6, 6)]:
    output[r][c] = colors[0]
  for r, c in [(3, 5), (3, 6), (4, 5), (4, 6), (5, 3), (5, 4), (6, 3), (6, 4)]:
    output[r][c] = colors[1]
  if flip:
    grid, output = common.flip(grid), common.flip(output)
  if xpose:
    grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 7], flip=True, xpose=True),
      generate(colors=[4, 8], flip=False, xpose=False),
      generate(colors=[3, 2], flip=False, xpose=True),
  ]
  test = [
      generate(colors=[9, 1], flip=True, xpose=False),
  ]
  return {"train": train, "test": test}
