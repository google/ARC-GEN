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


def generate(rows=None, cols=None, heights=None, colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    heights: a list of heights for the different boxes
    colors: digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    # A pair of heights
    heights = [5, common.randint(4, 5)]
    # If second height is 4 units, we sometimes increase the first to 6
    heights[0] = heights[0] if heights[1] > 4 or common.randint(0, 3) else 6
    # Rows start out at <0, max> ... but sometimes we shift the top box downward
    rows = [0, size - heights[1]]
    if heights[0] + heights[1] < size and common.randint(0, 1) == 0:
      rows[0] += 1
    # Columns are easy
    cols = [common.randint(0, 1), 4]
    # Any two colors besides blue
    colors = common.random_colors(2, exclude=[common.blue()])
    # Every so often, we drop the second box
    if common.randint(0, 3) == 0:
      rows.pop()
      cols.pop()
      heights.pop()
      colors.pop()

  grid, output = common.grids(size, size)
  for row, col, height, color in zip(rows, cols, heights, colors):
    grid[row + height // 2][col + 2] = color
    for r in range(row, row + height):
      for c in range(col, col + 5):
        output[r][c] = color
        if (r == row + 1 and c != col + 2) or r == row + height - 1:
          output[r][c] = grid[r][c] = common.blue()
      if r == row: continue
      for c in [col, col + 4]:
        output[r][c] = grid[r][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0], cols=[1], heights=[6], colors=[2]),
      generate(rows=[1, 6], cols=[1, 4], heights=[5, 4], colors=[2, 3]),
      generate(rows=[0, 6], cols=[1, 4], heights=[5, 4], colors=[6, 8]),
  ]
  test = [
      generate(rows=[0, 5], cols=[0, 4], heights=[5, 5], colors=[4, 7]),
  ]
  return {"train": train, "test": test}
