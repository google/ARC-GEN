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


def generate(width=None, height=None, col=None, length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    col: The column of the line.
    length: The length of the line.
  """

  if width is None:
    width, height = common.randint(6, 9), common.randint(10, 15)
    col = common.randint(1, width - 2)
    length = common.randint(3, 8)

  grid, output = common.grids(width, height)
  for r in range(length):
    output[r][col] = grid[r][col] = 5
  for c in range(width):
    for r in range(0, min(height, length + 2 * (col - c))):
      if c < col: output[r][c] = 8
      if c > col: output[r][c] = 6
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=11, col=2, length=4),
      generate(width=7, height=14, col=3, length=5),
      generate(width=8, height=14, col=4, length=7),
  ]
  test = [
      generate(width=9, height=15, col=3, length=7),
  ]
  return {"train": train, "test": test}
