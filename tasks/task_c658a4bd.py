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


def generate(size=None, widths=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    widths: The widths of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the boxes.
  """

  def draw():
    out_width = max(widths)
    grid, output = common.grid(size, size), common.grid(out_width, out_width)
    for width, row, col, color in zip(widths, rows, cols, colors):
      common.hollow_rect(grid, width, width, row, col, color)
      coord = (out_width - width) // 2
      common.hollow_rect(output, width, width, coord, coord, color)
    return grid, output

  def check_one_side_visible(grid):
    for width, row, col, color in zip(widths, rows, cols, colors):
      is_vis = True
      for r in range(row, row + width):
        is_vis = is_vis and common.get_pixel(grid, r, col) == color
      if is_vis: continue
      is_vis = True
      for r in range(row, row + width):
        is_vis = is_vis and common.get_pixel(grid, r, col + width - 1) == color
      if is_vis: continue
      is_vis = True
      for c in range(col, col + width):
        is_vis = is_vis and common.get_pixel(grid, row, c) == color
      if is_vis: continue
      is_vis = True
      for c in range(col, col + width):
        is_vis = is_vis and common.get_pixel(grid, row + width - 1, c) == color
      if is_vis: continue
      return False
    return True

  if size is None:
    out_width = common.randint(7, 10)
    size = 3 * out_width - 11
    widths = common.shuffle(range(out_width, 0, -2))
    colors = common.random_colors(len(widths))
    while True:
      rows = [common.randint(0, size - w + 2) - 1 for w in widths]
      cols = [common.randint(0, size - w + 2) - 1 for w in widths]
      grid, _ = draw()
      if check_one_side_visible(grid): break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, widths=[1, 5, 3, 7, 9], rows=[2, 1, 2, 7, 9],
               cols=[0, 3, 10, 1, 5], colors=[2, 4, 1, 8, 3]),
      generate(size=13, widths=[6, 8, 4, 2], rows=[1, 4, 1, 9],
               cols=[0, 3, 8, 0], colors=[8, 2, 3, 4]),
  ]
  test = [
      generate(size=19, widths=[10, 8, 6, 2, 4], rows=[1, 5, 3, 2, 14],
               cols=[2, 5, 4, 15, 11], colors=[6, 3, 8, 2, 4]),
  ]
  return {"train": train, "test": test}
