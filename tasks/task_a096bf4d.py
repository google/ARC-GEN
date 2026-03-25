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


def generate(width=None, height=None, bgcolor=None, fgcolor=None, active=None,
             rows=None, cols=None, cells=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bgcolor: The background color.
    fgcolor: The foreground color.
    active: The active cells in the 2x2 block.
    rows: The row indices of the special cells.
    cols: The column indices of the special cells.
    cells: The active indices of the special cells.
    colors: The colors of the special cells.
  """

  def draw():
    if 0 not in rows or 0 not in cols: return None, None
    if height - 1 not in rows or width - 1 not in cols: return None, None
    grid, output = common.grids(5 * width + 1, 5 * height + 1)
    # First, draw the sqaures and the insides.
    for row in range(height):
      for col in range(width):
        common.rect(grid, 4, 4, 5 * row + 1, 5 * col + 1, bgcolor)
        common.rect(output, 4, 4, 5 * row + 1, 5 * col + 1, bgcolor)
        for r in range(2):
          for c in range(2):
            if r * 2 + c not in active: continue
            rr, cc = 5 * row + 2 + r, 5 * col + 2 + c
            output[rr][cc] = grid[rr][cc] = fgcolor
    # Second, draw the given special cells.
    for row, col, cell, color in zip(rows, cols, cells, colors):
      r, c = cell // 2, cell % 2
      rr, cc = 5 * row + 2 + r, 5 * col + 2 + c
      if output[rr][cc] != fgcolor: return None, None
      output[rr][cc] = grid[rr][cc] = color
    # Third, connect special cells of the same color.
    for i, (row_i, col_i, cell_i, color_i) in enumerate(zip(rows, cols, cells, colors)):
      for j, (row_j, col_j, cell_j, color_j) in enumerate(zip(rows, cols, cells, colors)):
        if i == j: continue
        if color_i != color_j: continue
        r, c = cell_i // 2, cell_j % 2
        if row_i == row_j:
          if abs(col_i - col_j) <= 1: return None, None
          for col in range(col_i + 1, col_j):
            rr, cc = 5 * row_i + 2 + r, 5 * col + 2 + c
            if output[rr][cc] != fgcolor: return None, None
            output[rr][cc] = color_i
        if col_i == col_j:
          if abs(row_i - row_j) <= 1: return None, None
          for row in range(row_i + 1, row_j):
            rr, cc = 5 * row + 2 + r, 5 * col_i + 2 + c
            if output[rr][cc] != fgcolor: return None, None
            output[rr][cc] = color_i
    return grid, output

  if width is None:
    width, height = common.randint(3, 5), common.randint(3, 5)
    bgcolor = common.random_color()
    fgcolor = common.random_color(exclude=[bgcolor])
    num_colors = common.randint(1, 4)
    while True:
      active = common.sample([0, 1, 2, 3], common.randint(3, 4))
      subset = common.random_colors(num_colors, exclude=[bgcolor, fgcolor])
      rows, cols, cells, colors = [], [], [], []
      for color in subset:
        cell = common.choice(active)
        wide, tall = common.randint(2, width), common.randint(2, height)
        brow = common.randint(0, height - tall)
        bcol = common.randint(0, width - wide)
        if common.randint(0, 1):  # Pick three corners
          corners = common.sample([0, 1, 2, 3], 3)
        else:  # Pick two corners, but not diagonally opposite
          while True:
            corners = common.sample([0, 1, 2, 3], 2)
            if 0 in corners and 3 in corners: continue
            if 1 in corners and 2 in corners: continue
            break
        if 0 in corners: rows, cols = rows + [brow], cols + [bcol]
        if 1 in corners: rows, cols = rows + [brow], cols + [bcol + wide - 1]
        if 2 in corners: rows, cols = rows + [brow + tall - 1], cols + [bcol]
        if 3 in corners: rows, cols = rows + [brow + tall - 1], cols + [bcol + wide - 1]
        cells += [cell] * len(corners)
        colors += [color] * len(corners)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=5, bgcolor=2, fgcolor=3, active=[0, 1, 2, 3],
               rows=[0, 0, 0, 2, 3, 4, 4], cols=[0, 1, 2, 2, 1, 0, 3],
               cells=[2, 0, 2, 2, 0, 1, 1], colors=[1, 6, 1, 1, 6, 8, 8]),
      generate(width=4, height=4, bgcolor=1, fgcolor=8, active=[1, 2, 3],
               rows=[0, 0, 0, 3], cols=[0, 1, 3, 1], cells=[3, 1, 3, 1],
               colors=[2, 4, 2, 4]),
      generate(width=3, height=3, bgcolor=8, fgcolor=4, active=[0, 1, 2],
               rows=[0, 1, 1, 2], cols=[1, 0, 2, 1], cells=[0, 2, 2, 0],
               colors=[7, 3, 3, 7]),
  ]
  test = [
      generate(width=5, height=5, bgcolor=5, fgcolor=2, active=[0, 1, 3],
               rows=[0, 0, 1, 1, 3, 3, 4, 4, 4, 4],
               cols=[0, 2, 1, 3, 0, 3, 0, 2, 3, 4],
               cells=[3, 1, 3, 3, 3, 3, 0, 1, 0, 1],
               colors=[8, 3, 4, 4, 8, 8, 6, 3, 6, 3]),
  ]
  return {"train": train, "test": test}
