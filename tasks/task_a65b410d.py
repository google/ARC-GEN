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


def generate(width=None, height=None, row=None, length=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width the grid
    height: the height the grid
    row: the row with the "red" line
    length: the length of the "red" line
  """
  if width is None:
    triangle = common.randint(3, 9)
    width = triangle + common.randint(1, 4)
    height = triangle + common.randint(1, 4)
    length = common.randint(2, triangle - 1)
    row = triangle - length

  grid, output = common.grids(width, height)
  for c in range(length):
    output[row][c] = grid[row][c] = common.red()
  for r in range(row):
    for c in range(length + row - r):
      output[r][c] = common.green()
  for r in range(row + 1, row + length):
    for c in range(length + row - r):
      output[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7, row=3, length=2),
      generate(width=9, height=8, row=3, length=3),
      generate(width=9, height=7, row=2, length=4),
  ]
  test = [
      generate(width=9, height=9, row=2, length=5),
  ]
  return {"train": train, "test": test}
