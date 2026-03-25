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


def generate(rows=None, cols=None, widths=None, heights=None, colors=None,
             boxes=3, size=15):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    widths: a list of box widths
    heights: a list of box heights
    colors: a list of colors to be used
    boxes: the number of boxes to be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    while True:
      widths, heights = common.randints(2, 7, boxes), common.randints(2, 7, boxes)
      rows = [common.randint(1, size - height - 1) for height in heights]
      cols = [common.randint(1, size - width - 1) for width in widths]
      if common.overlaps(rows, cols, widths, heights, 2): continue
      colors = [common.pink()] * boxes
      newrows, newcols, newwidths, newheights = [], [], [], []
      for row, col, width, height in zip(rows, cols, widths, heights):
        w, t = common.randint(0, width - 2), common.randint(0, height - 2)
        if not w or not t: continue
        r = row + common.randint(1, height - t - 1)
        c = col + common.randint(1, width - w - 1)
        newrows, newcols = newrows + [r], newcols + [c]
        newwidths, newheights = newwidths + [w], newheights + [t]
      if sum(w * t for w, t in zip(newwidths, newheights)) < 2 * boxes: continue
      rows, cols = rows + newrows, cols + newcols
      widths, heights = widths + newwidths, heights + newheights
      colors.extend([common.yellow()] * len(newrows))
      break

  grid, output = common.grids(size, size, common.cyan())
  for row, col, width, height, color in zip(rows, cols, widths, heights, colors):
    for r in range(row - 1, row + height + 1):
      for c in range(col - 1, col + width + 1):
        if color == common.pink(): output[r][c] = common.green()
        if r < row or r >= row + height or c < col or c >= col + width: continue
        grid[r][c] = color if color == common.pink() else common.cyan()
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [generate(rows=[2, 4, 10, 3], cols=[8, 3, 5, 9], widths=[4, 2, 4, 2],
                    heights=[5, 2, 4, 3], colors=[6, 6, 6, 4]),
           generate(rows=[1, 3, 8, 4, 9], cols=[8, 2, 8, 3, 9],
                    widths=[3, 4, 6, 1, 4], heights=[3, 4, 6, 2, 4],
                    colors=[6, 6, 6, 4, 4])]
  test = [generate(rows=[2, 3, 11, 4, 4, 12], cols=[9, 2, 4, 10, 3, 6],
                   widths=[3, 4, 7, 1, 2, 2], heights=[6, 4, 3, 3, 2, 1],
                   colors=[6, 6, 6, 4, 4, 4])]
  return {"train": train, "test": test}
