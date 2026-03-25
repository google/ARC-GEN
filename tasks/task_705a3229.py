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


def generate(width=None, height=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  if width is None:
    width, height = common.randint(8, 16), common.randint(8, 16)
    rows, cols = [], []
    while not rows:
      lb_width, lb_height = (width + 1) // 2, (height + 1) // 2
      ub_width, ub_height = (width - 2) // 2, (height - 2) // 2
      if common.randint(0, 1):
        rows.append(common.randint(1, ub_height))
        cols.append(common.randint(1, ub_width))
      if common.randint(0, 1):
        rows.append(common.randint(1, ub_height))
        cols.append(common.randint(lb_width, width - 2))
      if common.randint(0, 1):
        rows.append(common.randint(lb_height, height - 2))
        cols.append(common.randint(1, ub_width))
      if common.randint(0, 1):
        rows.append(common.randint(lb_height, height - 2))
        cols.append(common.randint(lb_width, width - 2))
    colors = common.random_colors(len(rows))

  grid, output = common.grids(width, height)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
    rdir, cdir = -1 if row < height // 2 else 1, -1 if col < width // 2 else 1
    for dr in range(height):
      common.draw(output, row + dr * rdir, col, color)
    for dc in range(width):
      common.draw(output, row, col + dc * cdir, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=12, rows=[3, 4, 8], cols=[2, 6, 7],
               colors=[8, 4, 5]),
      generate(width=15, height=14, rows=[4, 11], cols=[9, 5], colors=[3, 5]),
      generate(width=8, height=11, rows=[4], cols=[4], colors=[9]),
      generate(width=12, height=12, rows=[2, 10], cols=[3, 9], colors=[8, 3]),
  ]
  test = [
      generate(width=16, height=11, rows=[1, 2, 6, 7], cols=[13, 4, 5, 11],
               colors=[3, 8, 6, 5]),
  ]
  return {"train": train, "test": test}
