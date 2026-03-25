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


def generate(size=None, color_map=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the 
    color_map: A map of column indices.
    colors: The colors of the grid.
  """

  if size is None:
    size = 5 if common.randint(0, 5) else 6
    # First, figure out the widths of the inner sub-figures.
    while True:
      widths = [common.randint(1, 2 if size == 5 else 3) for _ in range(9)]
      if sum(widths[0:3]) != size: continue
      if sum(widths[3:6]) != size: continue
      if sum(widths[6:9]) != size: continue
      if widths[0] + widths[4] + widths[8] == size: break
    # Second, figure out the column indices in the color map.
    color_map = []
    col = 0
    for c in range(widths[0]):
      color_map.append(col + c)
    col = size + 1 + widths[3]
    for c in range(widths[4]):
      color_map.append(col + c)
    col = 2 * (size + 1) + widths[6] + widths[7]
    for c in range(widths[8]):
      color_map.append(col + c)
    # Third, figure out the colors (no two adjacent should have the same color).
    subsets = []
    for _ in range(3):
      while True:
        subset = common.choices([0, 1, 2, 3, 4, 5, 8, 9], 3)
        if subset[0] != subset[1] and subset[1] != subset[2]: break
      subsets.extend(subset)
    # Fourth, figure out the contents and render them.
    wide = 3 * size + 2
    grid = common.grid(wide, size, 7)
    col = -1
    for index, (width, color) in enumerate(zip(widths, subsets)):
      if index % 3 == 0: col += 1  # Account for the pink separators.
      while True:  # We need a connected shape that covers certain columns.
        coords = [(r, c) for r in range(size) for c in range(width)]
        coords = common.sample(coords, common.randint(1, len(coords) - 1))
        columns = set([c for _, c in coords])
        if index % 3 == 0 and width - 1 not in columns: continue
        if index % 3 == 1 and len(columns) != width: continue
        if index % 3 == 2 and 0 not in columns: continue
        if common.connected(coords): break
      for r, c in coords:
        grid[r][col + c] = color
      col += width
    # Fifth, draw the pink separators.
    for r in range(size):
      grid[r][2 * size + 1] = grid[r][size] = 6
    colors = common.flatten(grid)

  wide = 3 * size + 2
  grid, output = common.grid(wide, size), common.grid(size, size)
  for i, color in enumerate(colors):
    grid[i // wide][i % wide] = color
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][color_map[c]]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, color_map=[0, 1, 8, 15, 16],
               colors=[7, 7, 4, 7, 8, 6, 7, 7, 8, 7, 7, 6, 5, 7, 7, 9, 7,
                       7, 7, 4, 4, 8, 6, 2, 2, 8, 3, 3, 6, 5, 5, 7, 9, 7,
                       2, 2, 4, 7, 8, 6, 7, 2, 8, 3, 7, 6, 7, 5, 0, 9, 9,
                       7, 7, 4, 4, 8, 6, 2, 2, 8, 3, 3, 6, 5, 5, 0, 7, 9,
                       7, 7, 4, 7, 8, 6, 7, 7, 8, 7, 7, 6, 5, 7, 0, 7, 9]),
      generate(size=5, color_map=[0, 1, 8, 15, 16],
               colors=[7, 7, 1, 8, 8, 6, 7, 7, 7, 7, 7, 6, 4, 7, 7, 7, 7,
                       8, 8, 1, 8, 8, 6, 2, 2, 9, 4, 4, 6, 4, 0, 0, 1, 1,
                       8, 7, 1, 7, 7, 6, 2, 2, 9, 4, 4, 6, 4, 0, 0, 7, 1,
                       8, 8, 7, 7, 7, 6, 7, 7, 7, 7, 4, 6, 7, 0, 0, 1, 1,
                       7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 4, 6, 7, 7, 7, 1, 7]),
      generate(size=5, color_map=[0, 1, 8, 15, 16],
               colors=[7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7,
                       7, 9, 3, 1, 7, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 6, 7, 8, 5, 6, 7, 6, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 4, 0, 2, 7,
                       7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7]),
  ]
  test = [
      generate(size=5, color_map=[0, 1, 8, 15, 16],
               colors=[4, 4, 9, 9, 7, 6, 8, 8, 7, 7, 7, 6, 2, 2, 7, 7, 7,
                       4, 7, 9, 9, 7, 6, 7, 8, 7, 7, 7, 6, 7, 2, 7, 9, 9,
                       4, 4, 7, 7, 2, 6, 8, 8, 7, 9, 9, 6, 2, 2, 5, 7, 9,
                       7, 4, 7, 7, 2, 6, 8, 7, 2, 7, 9, 6, 7, 2, 7, 9, 9,
                       4, 4, 7, 7, 2, 6, 8, 8, 7, 9, 9, 6, 2, 2, 7, 7, 7]),
      generate(size=5, color_map=[0, 1, 2, 9, 16],
               colors=[7, 7, 1, 8, 2, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7,
                       7, 7, 1, 8, 2, 6, 7, 7, 7, 7, 7, 6, 7, 7, 7, 4, 3,
                       7, 7, 7, 8, 2, 6, 7, 7, 7, 9, 7, 6, 7, 7, 5, 4, 3,
                       7, 7, 7, 7, 2, 6, 7, 7, 8, 9, 3, 6, 7, 7, 5, 4, 3,
                       7, 7, 7, 7, 7, 6, 7, 7, 8, 9, 3, 6, 7, 7, 7, 7, 3]),
      generate(size=6, color_map=[0, 1, 9, 10, 11, 19],
               colors=[7, 1, 8, 3, 3, 3, 6, 9, 9, 2, 2, 7, 7, 6, 5, 7, 7, 7, 7, 7,
                       7, 1, 7, 7, 7, 3, 6, 9, 7, 7, 2, 7, 7, 6, 7, 8, 8, 7, 7, 7,
                       7, 1, 7, 7, 7, 3, 6, 9, 7, 7, 2, 7, 7, 6, 7, 7, 8, 7, 7, 7,
                       1, 1, 7, 7, 7, 3, 6, 9, 7, 7, 2, 7, 9, 6, 7, 7, 8, 8, 8, 7,
                       7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 2, 7, 9, 6, 7, 7, 7, 7, 8, 7,
                       7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 2, 2, 9, 6, 7, 7, 7, 7, 7, 5]),
  ]
  return {"train": train, "test": test}
