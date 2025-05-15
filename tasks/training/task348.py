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


def generate(width=None, height=None, col=None, length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    col: the column of the line
    length: the length of the line
  """
  if width is None:
    width, height = common.randint(5, 10), common.randint(5, 10)
    col = common.randint(2, width - 3)
    length = common.randint(3, height - 1)

  grid, output = common.grids(width, height)
  for r in range(length):
    output[r][col] = grid[r][col] = common.orange()
  for c in range(col, width):
    for r in range(length - (c - col)):
      output[r][c] = common.orange() if c % 2 == col % 2 else common.cyan()
  for c in range(col):
    for r in range(length - (col - c)):
      output[r][c] = common.orange() if c % 2 == col % 2 else common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=5, col=3, length=4),
      generate(width=8, height=7, col=2, length=5),
  ]
  test = [
      generate(width=9, height=9, col=5, length=7),
  ]
  return {"train": train, "test": test}
