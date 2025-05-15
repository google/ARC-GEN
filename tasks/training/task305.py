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
             size=16):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    widths: a list of widths of the cutouts
    heights: a list of heights of the cutouts
    colors: how many colors of stripes to use
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    for r in range(size):
      for c in range(size):
        output[r][c] = grid[r][c] = (r + c) % colors + 1
    for row, col, width, height in zip(rows, cols, widths, heights):
      for r in range(row, row + height):
        for c in range(col, col + width):
          grid[r][c] = common.black()
    # Ensures that each color is visible.
    for c in range(size):
      col = [grid[r][c] for r in range(size) if grid[r][c]]
      if len(set(col)) != colors: return False
    for r in range(size):
      row = [grid[r][c] for c in range(size) if grid[r][c]]
      if len(set(row)) != colors: return False
    return True

  if rows is None:
    while True:
      widths = [common.randint(2, 4) for _ in range(5)]
      heights = [common.randint(2, 4) for _ in range(5)]
      rows = [common.randint(0, size - h) for h in heights]
      cols = [common.randint(0, size - w) for w in widths]
      colors = common.randint(4, 9)
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 5, 9, 11, 12], cols=[1, 12, 10, 6, 6],
               widths=[3, 2, 4, 3, 4], heights=[4, 2, 3, 4, 3], colors=5),
      generate(rows=[2, 3, 6, 7, 9], cols=[6, 5, 8, 8, 0],
               widths=[2, 3, 3, 4, 4], heights=[3, 2, 4, 3, 4], colors=6),
      generate(rows=[2, 8, 10, 12], cols=[1, 1, 12, 11],
               widths=[4, 4, 2, 4], heights=[4, 2, 2, 3], colors=7),
  ]
  test = [
      generate(rows=[0, 4, 5, 12], cols=[7, 2, 5, 7],
               widths=[3, 4, 4, 2], heights=[2, 4, 4, 2], colors=8),
  ]
  return {"train": train, "test": test}
