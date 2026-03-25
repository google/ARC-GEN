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


def generate(width=None, height=None, row=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    row: The row of the line.
    cols: The columns of the pixels.
  """

  if width is None:
    width, height = common.randint(10, 25), common.randint(8, 21)
    row = common.randint(1, height // 2)
    cols = []
    mod = 0
    for c in range(width):
      if c % 2 == mod: cols.append(c)
      if common.randint(0, 3) == 0: mod = (mod + 1) % 2

  grid, output = common.grids(width, height, 3)
  for col in cols:
    output[row][col] = grid[row][col] = 7
  color = 0
  for r in range(row + 2, height, 2):
    for c in range(1, width - 1):
      if output[r - 2][c - 1] != 3 and output[r - 2][c] == 3 and output[r - 2][c + 1] != 3:
        output[r][c] = 6 + color % 2
    color += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=11, row=1, cols=[0, 2, 4, 6, 8, 9, 11, 13, 15]),
      generate(width=16, height=13, row=2, cols=[0, 1, 2, 4, 6, 8, 9, 11, 13, 14, 15]),
      generate(width=16, height=9, row=4, cols=[3, 5, 6, 7, 9, 10, 12, 13, 15]),
  ]
  test = [
      generate(width=15, height=13, row=2, cols=[2, 4, 5, 6, 7, 8, 9, 10, 12]),
      generate(width=17, height=21, row=2, cols=[0, 2, 4, 6, 8, 10, 12, 14, 16]),
      generate(width=24, height=10, row=2, cols=[3, 4, 5, 7, 9, 11, 12, 14, 16, 18, 19, 21]),
  ]
  return {"train": train, "test": test}
