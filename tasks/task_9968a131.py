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


def generate(size=None, row=None, col=None, length=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    row: The row where the pattern starts.
    col: The column where the pattern starts.
    length: The length of the pattern.
    colors: The colors of the pattern.
  """

  if size is None:
    size = common.randint(4, 6)
    length = common.randint(3, size)
    row = common.randint(0, size - length)
    col = common.randint(0, size - 3)
    colors = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], 2)

  grid, output = common.grids(size, size, 7)
  for i in range(length):
    r, c = row + i, col
    grid[r][c + i % 2] = colors[0]
    grid[r][c + 1 - i % 2] = colors[1]
    if i % 2: c += 1
    output[r][c + i % 2] = colors[0]
    output[r][c + 1 - i % 2] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, row=0, col=1, length=4, colors=[3, 8]),
      generate(size=6, row=0, col=0, length=6, colors=[0, 5]),
  ]
  test = [
      generate(size=5, row=1, col=1, length=3, colors=[2, 9]),
  ]
  return {"train": train, "test": test}
