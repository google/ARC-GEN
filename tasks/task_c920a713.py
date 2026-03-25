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


def generate(size=None, widths=None, heights=None, rows=None, cols=None,
             colors=None, extra_row=None, extra_col=None, extra_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    widths: The widths of the boxes.
    heights: The heights of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the boxes.
    extra_row: The row of the extra pixel.
    extra_col: The column of the extra pixel.
    extra_color: The color of the extra pixel.
  """

  def draw():
    out_width = 2 * len(widths) - 1
    grid, output = common.grid(size, size), common.grid(out_width, out_width)
    for i in range(len(widths)):
      width, height, row, col, color = widths[i], heights[i], rows[i], cols[i], colors[i]
      common.hollow_rect(grid, width, height, row, col, color)
      common.hollow_rect(output, out_width - 2 * i, out_width - 2 * i, i, i, color)
    if extra_color: grid[extra_row][extra_col] = extra_color
    return grid, output

  def check_dominance():
    cells_to_boxes = {}
    # First, mark all the cells where boxes are.
    for i in range(len(widths)):
      width, height, row, col = widths[i], heights[i], rows[i], cols[i]
      for r in range(row, row + height):
        cell = (r, col)
        if cell not in cells_to_boxes: cells_to_boxes[cell] = []
        cells_to_boxes[cell].append(i)
        cell = (r, col + width - 1)
        if cell not in cells_to_boxes: cells_to_boxes[cell] = []
        cells_to_boxes[cell].append(i)
      for c in range(col, col + width):
        cell = (row, c)
        if cell not in cells_to_boxes: cells_to_boxes[cell] = []
        cells_to_boxes[cell].append(i)
        cell = (row + height - 1, c)
        if cell not in cells_to_boxes: cells_to_boxes[cell] = []
        cells_to_boxes[cell].append(i)
    # Second, check if every adjacent pair has a "special" overlapping cell.
    for i in range(1, len(widths)):
      good = False
      for boxes in cells_to_boxes.values():
        if sorted(boxes) == [i - 1, i]: good = True
      if not good: return False
    # Third, check that each box has at least three corners showing.
    for i in range(0, len(widths)):
      width, height, row, col = widths[i], heights[i], rows[i], cols[i]
      showing = 0
      if cells_to_boxes[(row, col)][-1] == i: showing += 1
      if cells_to_boxes[(row + height - 1, col)][-1] == i: showing += 1
      if cells_to_boxes[(row, col + width - 1)][-1] == i: showing += 1
      if cells_to_boxes[(row + height - 1, col + width - 1)][-1] == i: showing += 1
      if showing < 3: return False
    return True

  if size is None:
    size, num_boxes = common.randint(12, 25), common.randint(3, 7)
    colors = common.random_colors(num_boxes)
    while True:
      widths = [common.randint(3, size - 3) for _ in range(num_boxes)]
      heights = [common.randint(3, size - 3) for _ in range(num_boxes)]
      rows = [common.randint(0, size - h) for h in heights]
      cols = [common.randint(0, size - w) for w in widths]
      if check_dominance(): break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, widths=[9, 7, 6, 5, 8], heights=[6, 4, 5, 11, 10],
               rows=[6, 6, 4, 3, 9], cols=[6, 0, 4, 7, 10],
               colors=[5, 2, 3, 1, 7]),
      generate(size=12, widths=[6, 9, 5, 4, 5], heights=[4, 9, 5, 6, 3],
               rows=[8, 2, 5, 2, 1], cols=[2, 0, 5, 4, 1],
               colors=[8, 1, 4, 2, 3]),
      generate(size=25, widths=[7, 18, 7, 8, 9, 12], heights=[10, 11, 7, 7, 9, 9],
               rows=[2, 6, 16, 14, 14, 9], cols=[1, 1, 1, 6, 12, 4],
               colors=[2, 4, 3, 9, 7, 5], extra_row=16, extra_col=13,
               extra_color=4),
  ]
  test = [
      generate(size=25, widths=[8, 13, 6, 13, 6, 7, 9],
               heights=[9, 13, 6, 9, 8, 3, 9],
               rows=[2, 7, 15, 9, 15, 20, 15], cols=[16, 6, 18, 8, 5, 9, 13],
               colors=[2, 3, 8, 5, 1, 4, 6]),
  ]
  return {"train": train, "test": test}
