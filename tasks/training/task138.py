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


def generate(width=None, height=None, left=None, right=None, up=None, down=None,
             draworder=None, colors=None, drawcolor=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    left: the left line column
    right: the right line column
    up: the top line row
    down: the bottom line row
    draworder: the order in which to draw the lines
    colors: a list of line colors
    drawcolor: a digit representing a color to be used for pixels
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if width is None:
    width = common.randint(10, 25)
    height = width + common.randint(-1, 1)
    left = common.randint(1, width // 3 - 1)
    right = common.randint(2 * width // 3 + 1, width - 2)
    up = common.randint(1, height // 3 - 1)
    down = common.randint(2 * height // 3 + 1, height - 2)
    colors = common.random_colors(4)
    drawcolor = colors[common.randint(0, 3)]
    pixels = common.remove_neighbors(common.random_pixels(width, height, 0.1))
    rows, cols = zip(*pixels)
    draworder = common.shuffle(range(4))

  grid = common.grid(width, height)
  output = common.grid(right - left + 1, down - up + 1)
  for row, col in zip(rows, cols):
    grid[row][col] = drawcolor
    common.draw(output, row - up, col - left, drawcolor)
    r, c, dr, dc = row, col, 0, 0
    dc = dc if drawcolor != colors[0] else -1
    dc = dc if drawcolor != colors[1] else 1
    dr = dr if drawcolor != colors[2] else -1
    dr = dr if drawcolor != colors[3] else 1
    while True:
      if r <= up or r >= down or c <= left or c >= right: break
      output[r - up][c - left] = drawcolor
      r, c = r + dr, c + dc
  for idx in draworder:
    if idx == 0:
      for r in range(height):
        grid[r][left] = colors[idx]
        common.draw(output, r - up, 0, colors[idx])
    if idx == 1:
      for r in range(height):
        grid[r][right] = colors[idx]
        common.draw(output, r - up, right - left, colors[idx])
    if idx == 2:
      for c in range(width):
        grid[up][c] = colors[idx]
        common.draw(output, 0, c - left, colors[idx])
    if idx == 3:
      for c in range(width):
        grid[down][c] = colors[idx]
        common.draw(output, down - up, c - left, colors[idx])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=22, left=5, right=16, up=1, down=15,
               draworder=[2, 3, 0, 1], colors=[3, 8, 1, 2], drawcolor=2,
               rows=[0, 4, 5, 5, 6, 6, 7, 7, 8, 12, 12, 12, 14, 16, 17, 21, 21],
               cols=[9, 0, 0, 15, 3, 18, 9, 19, 14, 3, 7, 14, 6, 8, 0, 0, 20]),
      generate(width=12, height=12, left=2, right=9, up=2, down=9,
               draworder=[2, 0, 3, 1], colors=[4, 1, 8, 6], drawcolor=8,
               rows=[5, 5, 6, 6, 8, 8, 10, 11, 11],
               cols=[6, 11, 3, 6, 7, 11, 6, 1, 7]),
      generate(width=15, height=14, left=3, right=11, up=5, down=10,
               draworder=[2, 3, 0, 1], colors=[3, 4, 2, 8], drawcolor=4,
               rows=[0, 0, 1, 2, 3, 4, 4, 4, 6, 6, 6, 6, 8, 8, 8, 9, 9, 9, 11,
                     11, 12, 12, 13, 13],
               cols=[2, 7, 5, 6, 5, 10, 12, 14, 0, 4, 5, 7, 0, 8, 10, 0, 6, 10,
                     10, 14, 4, 7, 2, 9]),
  ]
  test = [
      generate(width=15, height=16, left=3, right=12, up=2, down=13,
               draworder=[2, 0, 1, 3], colors=[1, 2, 3, 8], drawcolor=1,
               rows=[0, 0, 1, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 10, 10, 11, 14, 15],
               cols=[5, 9, 7, 0, 5, 10, 0, 8, 14, 10, 9, 1, 4, 5, 7, 1, 4, 6]),
  ]
  return {"train": train, "test": test}
