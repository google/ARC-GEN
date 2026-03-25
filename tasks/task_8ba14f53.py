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


def generate(rows=None, cols=None, groups=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    groups: The groups of the pixels.
    colors: The colors of the groups.
  """

  def draw():
    grid, output = common.grid(9, 4), common.grid(3, 3)
    # First, draw the borders.
    for row, col, group in zip(rows, cols, groups):
      for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
          grid[row + r][col + c] = colors[group]
    # Seond, clear out the black pixels.
    for row, col in zip(rows, cols):
      grid[row][col] = 0
    # Third, draw the output.
    row, col = 0, 0
    for group in [0, 1]:
      num_pixels = groups.count(group)
      for _ in range(num_pixels):
        if col == 3: row, col = row + 1, 0
        if row >= 3: return None, None
        output[row][col] = colors[group]
        col += 1
      row, col = row + 1, 0
    return grid, output

  if rows is None:
    colors = common.random_colors(2)
    while True:
      widths = [common.randint(3, 5) for _ in range(2)]
      v_spaces = [common.randint(0, 1) for _ in range(2)]
      if sum(widths) + sum(v_spaces) > 9: continue
      heights = [common.randint(3, 4) for _ in range(2)]
      h_spaces = [common.randint(0, 4 - height) for height in heights]
      col, rows, cols, groups = 0, [], [], []
      for group in range(2):
        col += v_spaces[group]
        row = h_spaces[group]
        notch_row, notch_col, notch_dir = -1, -1, 0
        if widths[group] > 3 and heights[group] > 3:
          notch_row = common.randint(0, heights[group] - 3)
          notch_col = common.randint(0, widths[group] - 3)
          notch_dir = 2 * common.randint(0, 1) - 1
        for r in range(heights[group] - 2):
          for c in range(widths[group] - 2):
            if r == notch_row:
              if notch_dir == -1 and c < notch_col: continue
              if notch_dir == +1 and c > notch_col: continue
            rows.append(row + 1 + r)
            cols.append(col + 1 + c)
            groups.append(group)
        col += widths[group]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 1, 1, 2, 2, 2], cols=[1, 2, 6, 1, 2, 6],
               groups=[0, 0, 1, 0, 0, 1], colors=[3, 1]),
      generate(rows=[1, 2, 2, 2, 2], cols=[1, 1, 2, 6, 7],
               groups=[0, 0, 0, 1, 1], colors=[7, 8]),
      generate(rows=[1, 1, 1, 1, 2, 2], cols=[1, 2, 6, 7, 2, 6],
               groups=[0, 0, 1, 1, 0, 1], colors=[9, 5]),
      generate(rows=[1, 1], cols=[1, 5], groups=[0, 1], colors=[8, 6]),
      generate(rows=[1, 1, 1, 1, 2, 2, 2], cols=[2, 5, 6, 7, 5, 6, 7],
               groups=[0, 1, 1, 1, 1, 1, 1], colors=[4, 6]),
      generate(rows=[1, 1, 2, 2, 2], cols=[1, 5, 1, 5, 6],
               groups=[0, 1, 0, 1, 1], colors=[7, 8]),
  ]
  test = [
      generate(rows=[1, 1, 2, 2, 2], cols=[1, 7, 1, 2, 3],
               groups=[0, 1, 0, 0, 0], colors=[4, 7]),
  ]
  return {"train": train, "test": test}
