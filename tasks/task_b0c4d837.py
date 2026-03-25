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


def generate(base=None, water=None, space=None, row_gap=None, col_gap=None):
  """Returns input and output grids according to the given parameters.

  Args:
    base: the base of the cup
    water: the height of the water in pixels
    space: the height of the empty cup space in pixels
    row_gap: how many extra rows to add on the top
    col_gap: how many extra cols to add on the sides
  """
  if base is None:
    base = common.randint(4, 8)
    water = common.randint(1, 7)
    space = common.randint(1, 4)
    row_gap = common.randint(1, 2)
    col_gap = common.randint(1, 2)

  width, height = 2 * col_gap + base, water + space + row_gap + 1
  grid, output = common.grid(width, height), common.grid(3, 3)
  for c in range(col_gap, col_gap + base):
    grid[height - 1][c] = common.gray()
  for r in range(height - water - space - 1, height - 1):
    grid[r][col_gap] = grid[r][col_gap + base - 1] = common.gray()
    if r < height - water - 1: continue
    for c in range(col_gap + 1, col_gap + base - 1):
      grid[r][c] = common.cyan()
  output[0][0] = common.cyan() if space > 0 else 0
  output[0][1] = common.cyan() if space > 1 else 0
  output[0][2] = common.cyan() if space > 2 else 0
  output[1][2] = common.cyan() if space > 3 else 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(base=4, water=1, space=3, row_gap=1, col_gap=1),
      generate(base=5, water=3, space=4, row_gap=1, col_gap=2),
      generate(base=7, water=3, space=3, row_gap=2, col_gap=1),
      generate(base=5, water=4, space=2, row_gap=2, col_gap=2),
      generate(base=4, water=2, space=1, row_gap=1, col_gap=1),
      generate(base=5, water=2, space=2, row_gap=2, col_gap=1),
  ]
  test = [
      generate(base=5, water=6, space=1, row_gap=1, col_gap=2),
  ]
  return {"train": train, "test": test}
