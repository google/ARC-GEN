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
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    width, height = common.randint(3, 9), common.randint(3, 9)
    rows, cols, r = [], [], common.randint(0, 1)
    while r + 1 < height:
      rows.append(r)
      cols.append(common.randint(0, width - 2))
      r += common.randint(2, 3)
    colors = common.random_colors(len(rows))

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    for col in range(c, width):
      output[r][col] = color
    for row in range(r, height):
      output[row][width - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6, rows=[1, 3], cols=[2, 1], colors=[2, 3]),
      generate(width=3, height=3, rows=[1], cols=[1], colors=[6]),
      generate(width=6, height=6, rows=[1, 4], cols=[1, 3], colors=[8, 5]),
      generate(width=5, height=7, rows=[1, 3, 5], cols=[2, 1, 2],
               colors=[8, 7, 6]),
  ]
  test = [
      generate(width=8, height=7, rows=[0, 2, 4], cols=[3, 2, 5],
               colors=[8, 7, 2]),
  ]
  return {"train": train, "test": test}
