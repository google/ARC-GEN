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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    colors: a list of digits representing the colors to be used
  """
  rows, cols, wides, talls = [], [], [], []
  def bisect(bitmap, row, col, wide, tall):
    cut = common.randint(0, 2)  # 0: no cut, 1: horizontal cut, 2: vertical cut
    cut = cut if cut != 1 or tall > 2 else 0
    cut = cut if cut != 2 or wide > 2 else 0
    if cut == 0:
      rows.append(row)
      cols.append(col)
      wides.append(wide)
      talls.append(tall)
      return
    if cut == 1:
      cutline = common.randint(row + 1, row + tall - 2)
      bisect(bitmap, row, col, wide, cutline - row)
      bisect(bitmap, cutline + 1, col, wide, tall - (cutline - row) - 1)
      for i in range(wide):
        bitmap[cutline][col + i] = common.red()
      return
    if cut == 2:
      cutline = common.randint(col + 1, col + wide - 2)
      bisect(bitmap, row, col, cutline - col, tall)
      bisect(bitmap, row, cutline + 1, wide - (cutline - col) - 1, tall)
      for i in range(tall):
        bitmap[row + i][cutline] = common.red()
      return

  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    while True:
      rows, cols, wides, talls = [], [], [], []
      bitmap = common.grid(width, height)
      bisect(bitmap, 0, 0, width, height)
      min_area, max_area = width * height + 1, -1
      for wide, tall in zip(wides, talls):
        area = wide * tall
        if min_area > area: min_area = area
        if max_area < area: max_area = area
      if min_area < max_area: break
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      area = wide * tall
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          bitmap[r][c] = bitmap[r][c] if area != min_area else common.cyan()
          bitmap[r][c] = bitmap[r][c] if area != max_area else common.blue()
    colors = []
    for r in range(height):
      for c in range(width):
        colors.append(bitmap[r][c])

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      if colors[r * width + c] == common.red():
        grid[r][c] = colors[r * width + c]
      output[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=18,
               colors=[8, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0,
                       0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 2, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                       2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                       0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1]),
      generate(width=13, height=11,
               colors=[0, 0, 0, 0, 2, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1,
                       1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2,
                       1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
                       1, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1,
                       1, 1, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 2, 1, 1, 1, 1, 1, 1, 1, 1]),
      generate(width=16, height=11,
               colors=[0, 0, 0, 2, 8, 8, 8, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       2, 8, 8, 8, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2,
                       2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 8, 8, 8, 2, 1,
                       1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 8, 8, 8, 2, 1, 1, 1, 1,
                       1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1,
                       1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                       0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0,
                       0, 0, 2, 8, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                       8, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 8, 2,
                       0, 0, 0, 0, 0]),
      generate(width=16, height=15,
               colors=[0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 8, 8, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 8, 8, 0, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0,
                       0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0,
                       2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 2, 2, 2, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 2, 2, 2, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0,
                       0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0,
                       0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0]),
  ]
  test = [
      generate(width=16, height=13,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
                       2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0,
                       0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 8, 2, 0, 0, 0, 0, 0, 0, 2,
                       8, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 8, 2, 0,
                       0, 0, 8, 8, 8, 2, 0, 0, 0, 0, 0, 0, 2, 8, 2, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
