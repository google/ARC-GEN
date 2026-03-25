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


def generate(rows=None, cols=None, lengths=None, colors=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of lengths of size one or two
    colors: a list of red or blue colors
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_big_boxes = common.randint(5, 7)
    lengths = [2] * num_big_boxes
    while True:
      rows = [common.randint(0, size - 2) for _ in lengths]
      cols = [common.randint(0, size - 2) for _ in lengths]
      if not common.overlaps(rows, cols, lengths, lengths, 1): break
    colors = [common.red()] * num_big_boxes
    for i in range(common.randint(1, num_big_boxes - 2)):
      colors[i] = common.blue()
    # Now draw whatever we've got onto a bitmap.
    grid = common.grid(size, size)
    for row, col, length, color in zip(rows, cols, lengths, colors):
      for dr in range(length):
        for dc in range(length):
          grid[row + dr][col + dc] = color
    # Finally, add in some singletons as long as they don't touch the same color
    for r in range(size):
      for c in range(size):
        if grid[r][c] or common.randint(0, 2): continue  # Something's here.
        color = common.red() if common.randint(0, 1) else common.blue()
        touching = False
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(grid, r + dr, c + dc) == color: touching = True
        if touching: continue
        rows.append(r)
        cols.append(c)
        lengths.append(1)
        colors.append(color)
        grid[r][c] = color

  grid, output, big_blue = common.grid(size, size), common.grid(5, 1), 0
  for row, col, length, color in zip(rows, cols, lengths, colors):
    for dr in range(length):
      for dc in range(length):
        grid[row + dr][col + dc] = color
    if length == 2 and color == common.blue(): big_blue += 1
  for c in range(big_blue):
    output[0][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 4, 4, 5, 8, 8],
               cols=[4, 8, 1, 7, 0, 2, 5, 1, 8],
               lengths=[2, 1, 2, 2, 1, 2, 2, 1, 1],
               colors=[2, 1, 1, 2, 1, 2, 1, 1, 1]),
      generate(rows=[0, 0, 0, 1, 2, 3, 4, 4, 5, 8, 7, 7],
               cols=[0, 3, 8, 5, 3, 8, 1, 4, 8, 1, 3, 6],
               lengths=[2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2],
               colors=[1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1]),
      generate(rows=[0, 0, 1, 2, 3, 4, 4, 6, 7, 8, 7],
               cols=[0, 3, 7, 0, 1, 4, 7, 4, 1, 5, 7],
               lengths=[2, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2],
               colors=[2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 3, 4, 6, 6, 7, 7],
               cols=[5, 8, 0, 3, 5, 1, 0, 6, 0, 3],
               lengths=[2, 1, 2, 1, 2, 2, 1, 2, 2, 2],
               colors=[2, 1, 1, 1, 1, 2, 1, 2, 2, 1]),
  ]
  return {"train": train, "test": test}
