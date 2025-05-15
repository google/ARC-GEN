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


def generate(row=None, col=None, flip=None, size=6):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a list of vertical coordinates where a street should be placed
    col: a list of horizontal coordinates where a street should be placed
    flip: whether to flip the grid horizontally
    size: the size of the grid
  """
  if row is None:
    row, col = common.randint(2, 4), common.randint(2, 4)
    flip = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for i in range(size):
    if i < 2: grid[i][col], grid[row][i] = common.cyan(), common.red()
    output[i][col], output[row][i] = common.cyan(), common.red()
  output[row][col] = common.yellow()
  if flip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=2, col=4, flip=0),
      generate(row=3, col=4, flip=1),
  ]
  test = [
      generate(row=4, col=3, flip=0),
  ]
  return {"train": train, "test": test}
