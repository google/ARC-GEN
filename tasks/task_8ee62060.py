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


def generate(size=None, colors=None, cdir=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
    cdir: The direction of the columns.
  """

  if size is None:
    size = 2 * common.randint(4, 7)
    vals = common.random_colors(2)
    colors = [common.choice(vals) for _ in range(4)]
    pos = common.randint(0, 4)
    if pos < 4: colors[pos] = 0
    cdir = 1 if common.randint(0, 1) else -1

  grid, output = common.grids(size, size)
  row, col1, col2 = 0, 0 if cdir == 1 else size - 2, size - 2 if cdir == 1 else 0
  while row < size:
    output[row][col2] = grid[row][col1] = colors[0]
    output[row][col2 + 1] = grid[row][col1 + 1] = colors[1]
    output[row + 1][col2] = grid[row + 1][col1] = colors[2]
    output[row + 1][col2 + 1] = grid[row + 1][col1 + 1] = colors[3]
    row, col1, col2 = row + 2, col1 + 2 * cdir, col2 + -2 * cdir
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, colors=[2, 2, 3, 2], cdir=-1),
      generate(size=12, colors=[8, 0, 2, 2], cdir=1),
      generate(size=10, colors=[2, 1, 1, 0], cdir=1),
  ]
  test = [
      generate(size=14, colors=[1, 8, 8, 1], cdir=-1),
  ]
  return {"train": train, "test": test}
