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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             edgecolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    edgecolors: a list of digits representing the edge colors to be used
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    edgecolors = common.random_colors(4)
    bitmap = common.grid(width, height)
    # Ensure we don't have two cells of the same color in the same row/column.
    for idx in range(len(edgecolors)):
      num_cells = common.randint(1, 3)
      if idx in [0, 2]:
        rows = [common.randint(2, height - 3) for _ in range(num_cells)]
        cols = common.sample(range(2, width - 2), num_cells)
      if idx in [1, 3]:
        rows = common.sample(range(2, height - 2), num_cells)
        cols = [common.randint(2, width - 3) for _ in range(num_cells)]
      for r, c in zip(rows, cols):
        bitmap[r][c] = edgecolors[idx]
    # Add some garbage pixels.
    for _ in range(common.randint(1, 3)):
      r, c = common.randint(2, height - 3), common.randint(2, width - 3)
      bitmap[r][c] = common.random_color(exclude=edgecolors)
    # Convert the bitmap back to a list of rows and columns.
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid, output = common.grids(width, height)
  for r in range(1, height - 1):
    output[r][0] = grid[r][0] = edgecolors[3]
    output[r][width - 1] = grid[r][width - 1] = edgecolors[1]
  for c in range(1, width - 1):
    output[0][c] = grid[0][c] = edgecolors[0]
    output[height - 1][c] = grid[height - 1][c] = edgecolors[2]
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
    if color == edgecolors[0]: output[1][col] = color
    if color == edgecolors[1]: output[row][width - 2] = color
    if color == edgecolors[2]: output[height - 2][col] = color
    if color == edgecolors[3]: output[row][1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=10, rows=[2, 3, 4, 5, 6, 7, 7],
               cols=[10, 3, 7, 3, 5, 9, 11], colors=[3, 2, 7, 3, 8, 4, 2],
               edgecolors=[4, 3, 8, 2]),
      generate(width=12, height=12, rows=[2, 3, 4, 6, 8, 9, 9],
               cols=[9, 7, 4, 8, 3, 5, 8], colors=[7, 2, 3, 4, 8, 1, 7],
               edgecolors=[1, 4, 7, 2]),
      generate(width=11, height=14, rows=[2, 3, 4, 7, 9, 10],
               cols=[2, 8, 4, 3, 6, 2], colors=[2, 6, 8, 4, 8, 8],
               edgecolors=[6, 8, 3, 4]),
  ]
  test = [
      generate(width=17, height=14,
               rows=[2, 2, 3, 3, 5, 5, 5, 7, 9, 9, 9, 10, 10],
               cols=[7, 12, 3, 14, 6, 10, 13, 4, 5, 8, 14, 3, 11],
               colors=[8, 1, 2, 3, 1, 7, 8, 2, 6, 4, 4, 8, 1],
               edgecolors=[4, 2, 8, 1]),
  ]
  return {"train": train, "test": test}
