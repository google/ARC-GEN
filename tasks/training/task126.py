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


def generate(width=None, height=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where shooters should be placed
    cols: a list of horizontal coordinates where shooters should be placed
    colors: a list of digits representing the colors to be used
  """
  if rows is None:
    width, height = common.randint(5, 20), common.randint(5, 10)
    rows, cols, colors = [], [], []
    c, next_color = 1, common.random_color(exclude=[common.yellow()])
    while c + 2 < width:
      rows.append(common.randint(0, height - 3))
      cols.append(c)
      colors.append(next_color)
      next_color = common.random_color(exclude=[common.yellow()])
      c += 4 if next_color == colors[-1] else common.randint(3, 4)

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    for (dr, dc) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]:
      output[r + dr][c + dc] = grid[r + dr][c + dc] = color
    output[height - 1][c + 1] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=8, rows=[0, 2], cols=[1, 5], colors=[6, 6]),
      generate(width=5, height=5, rows=[0], cols=[1], colors=[3]),
      generate(width=7, height=5, rows=[1, 2], cols=[1, 4], colors=[8, 6]),
  ]
  test = [
      generate(width=11, height=7, rows=[0, 1, 2], cols=[1, 5, 8],
               colors=[5, 8, 3]),
  ]
  return {"train": train, "test": test}
