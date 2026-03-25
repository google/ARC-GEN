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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             prow=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the lines.
    cols: The columns of the lines.
    colors: The colors of the lines.
    prow: The row of the pixel.
    xpose: Whether to transpose the grid.
  """

  def draw():
    nonlocal prow, xpose
    grid, output = common.grids(width, height)
    for row, col, color in zip(rows, cols, colors):
      for r in range(3):
        common.draw(grid, row + r, col, color)
        common.draw(output, row + r, col, color)
    row, col, zags = prow, 0, 0
    grid[row][col] = 2
    while True:
      if row < 0 or col < 0 or row >= height or col >= width: return None, None
      output[row][col] = 2
      if col + 1 >= width: break
      if grid[row][col + 1] == 1 + 2 * xpose: row, zags = row - 1, zags + 1
      elif grid[row][col + 1] == 3 - 2 * xpose: row, zags = row + 1, zags + 1
      else: col += 1
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    if zags < 10: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(15, 30), common.randint(12, 13)
    lines = common.randint(4, 2 * width // 3)
    while True:
      rows = [common.randint(-1, height - 2) for _ in range(lines)]
      cols = [common.randint(2, width - 2) for _ in range(lines)]
      if common.overlaps(rows, cols, [2] * lines, [4] * lines): continue
      colors = [2 * common.randint(1, 2) - 1 for _ in range(lines)]
      prow, xpose = common.randint(3, height - 4), common.randint(0, 1)
      grid, output = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=22, height=12,
               rows=[4, 2, 6, 1, 5, 9, 2, 7, 6, 7, 4, 8, 3, 10],
               cols=[2, 4, 4, 6, 6, 6, 9, 9, 11, 14, 17, 17, 19, 19],
               colors=[1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3],
               prow=5, xpose=1),
      generate(width=22, height=12, rows=[2, 0, 2, -1, 4, 5, 3, 7, 1, 6],
               cols=[2, 5, 7, 9, 9, 12, 15, 15, 19, 19],
               colors=[3, 1, 1, 1, 1, 3, 3, 3, 1, 1], prow=3, xpose=1),
      generate(width=19, height=13, rows=[2, 3, 2, 4], cols=[3, 6, 9, 12],
               colors=[3, 1, 3, 3], prow=3, xpose=0),
      generate(width=22, height=12, rows=[2, 2, 2, 4, 4],
               cols=[6, 13, 20, 9, 17], colors=[3, 3, 1, 1, 1], prow=3,
               xpose=0),
  ]
  test = [
      generate(width=29, height=13,
               rows=[1, 2, 3, 3, 3, 5, 6, 6, 6, 8, 8, 8, 10],
               cols=[7, 22, 4, 10, 18, 2, 7, 14, 22, 4, 10, 18, 22],
               colors=[1, 1, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 1], prow=6, xpose=0),
  ]
  return {"train": train, "test": test}
