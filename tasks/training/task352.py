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
    width = common.randint(5, 10)
    height = width - common.randint(0, 1)
    rows, cols, colors, vals = [], [], [], common.shuffle(list(range(height)))
    for i, val in enumerate(vals):
      if common.randint(0, 1) == 0: continue
      overlaps = False
      for r, c in zip(rows, cols):
        overlaps = overlaps or (abs(r - i) < 2 and abs(c - val) < 2)
      if overlaps: continue
      color = common.random_color(exclude=[common.blue(), common.red()])
      rows.append(i)
      cols.append(val)
      colors.append(common.red() if common.randint(0, 1) else color)

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    if color == common.red():
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          common.draw(output, r + dr, c + dc, common.blue())
    output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=5, rows=[0, 1, 3], cols=[0, 3, 1],
               colors=[2, 2, 6]),
      generate(width=8, height=8, rows=[0, 2, 4, 6], cols=[7, 3, 6, 2],
               colors=[2, 3, 8, 2]),
      generate(width=5, height=4, rows=[1], cols=[1], colors=[2]),
  ]
  test = [
      generate(width=10, height=10, rows=[0, 1, 3, 5, 7, 9],
               cols=[8, 2, 7, 1, 5, 9], colors=[7, 2, 2, 7, 2, 5]),
  ]
  return {"train": train, "test": test}
