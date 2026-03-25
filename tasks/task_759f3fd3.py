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


def generate(size=None, row=None, col=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    row: The row of the T.
    col: The column of the T.
  """

  if size is None:
    size = common.randint(10, 20)
    row, col = common.randint(2, size - 3), common.randint(2, size - 3)

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      output[r][c] = 4 if (max(abs(row - r), abs(col - c)) % 2 == 0) else 0
  for i in range(size):
    output[row][i] = output[i][col] = grid[row][i] = grid[i][col] = 3
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, row=4, col=6),
      generate(size=20, row=5, col=7),
  ]
  test = [
      generate(size=12, row=8, col=6),
  ]
  return {"train": train, "test": test}
