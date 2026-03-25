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


def generate(width=None, height=None, rows=None, lefts=None, rights=None,
             cols=None, lows=None, highs=None, row_colors=None,
             col_colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates for flat sticks
    lefts: a list of left coordinates for flat sticks
    rights: a list of right coordinates for flat sticks
    cols: a list of horizontal coordinates for tall sticks
    lows: a list of low coordinates for tall sticks
    highs: a list of high coordinates for tall sticks
    row_colors: a list of digits representing colors for flat sticks
    col_colors: a list of digits representing colors for tall sticks
  """
  if width is None:
    width, height = 10 * common.randint(1, 3), 10 * common.randint(1, 3)
    success = False
    while not success:
      success = True
      rows, cols = [], []
      lefts, rights, lows, highs = [], [], [], []
      row_colors, col_colors = [], []
      # First, pick directions and ensure they all get unique corridors.
      for _ in range(5):
        direction = common.randint(0, 1)
        if direction == 0:
          row = common.randint(0, height - 1)
          if row in rows: success = False
          rows.append(row)
        else:
          col = common.randint(0, width - 1)
          if col in cols: success = False
          cols.append(col)
      # Second, pick endpoints, and prevent clobbering with other sticks.
      for _ in rows:
        left, right = common.randint(0, width - 1), common.randint(0, width - 1)
        if abs(right - left) < 2 or left in cols or right in cols:
          success = False
        lefts.append(min(left, right))
        rights.append(max(left, right))
      for _ in cols:
        low, high = common.randint(0, height - 1), common.randint(0, height - 1)
        if abs(high - low) < 2 or high or low in rows or high in rows:
          success = False
        lows.append(min(low, high))
        highs.append(max(low, high))
      # Finally, pick unique colors for each stick.
      for _ in rows:
        color = common.random_color()
        if color in row_colors or color in col_colors: success = False
        row_colors.append(color)
      for _ in cols:
        color = common.random_color()
        if color in row_colors or color in col_colors: success = False
        col_colors.append(color)

  grid, output = common.grids(width, height)
  for row, left, right, color in zip(rows, lefts, rights, row_colors):
    grid[row][left] = grid[row][right] = color
    for c in range(left, right + 1):
      output[row][c] = color
  for col, low, high, color in zip(cols, lows, highs, col_colors):
    grid[low][col] = grid[high][col] = color
    for r in range(low, high + 1):
      output[r][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=30, rows=[6, 20], lefts=[3, 2], rights=[11, 7],
               cols=[4, 6, 14], lows=[18, 2, 12], highs=[27, 13, 17],
               row_colors=[3, 5], col_colors=[6, 2, 8]),
      generate(width=10, height=20, rows=[4, 8, 14], lefts=[2, 2, 1],
               rights=[7, 5, 6], cols=[3, 5], lows=[2, 12], highs=[10, 18],
               row_colors=[3, 7, 8], col_colors=[4, 9]),
  ]
  test = [
      generate(width=20, height=20, rows=[3, 7, 14], lefts=[1, 7, 8],
               rights=[16, 13, 14], cols=[3, 9], lows=[1, 2], highs=[18, 9],
               row_colors=[2, 7, 8], col_colors=[3, 5]),
  ]
  return {"train": train, "test": test}
