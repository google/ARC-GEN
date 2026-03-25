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


def generate(width=None, height=None, rows=None, cols=None, bgcolors=None,
             colors=None, brows=None, bcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    bgcolors: a list of two colors representing the background stripes
    colors: a list of two colors for the dots / diagonals
    brows: a list of vertical coordinates where background stripes should be
    bcols: a list of horizontal coordinates where background stripes should be
  """

  def draw(grid, output):
    # First, draws the background stripes.
    for r in brows:
      for c in range(width):
        output[r][c] = grid[r][c] = bgcolors[1]
    for c in bcols:
      for r in range(height):
        output[r][c] = grid[r][c] = bgcolors[1]
    # Then, draw the output diagonals.
    for row, col in zip(rows, cols):
      for r in range(height):
        for c in range(width):
          if r + c != row + col and r - c != row - col: continue
          output[r][c] = colors[0] if grid[r][c] == bgcolors[0] else colors[1]
    # Finally, draw the input dots -- keep track of which colors we see.
    seen = set()
    for row, col in zip(rows, cols):
      seen.add(grid[row][col])
      grid[row][col] = colors[0] if grid[row][col] == bgcolors[0] else colors[1]
    return len(seen) == 2  # To be legal, we need to see two colors.

  if rows is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    bgcolors = common.random_colors(2)
    colors = common.random_colors(2, exclude=bgcolors)
    brows, bcols, row, col = [], [], common.randint(2, 7), common.randint(2, 7)
    while True:  # First, choose horizontal stripes.
      spacing = common.randint(2, 5)
      if row + spacing > height: break
      brows.extend(range(row, row + spacing))
      row += spacing + common.randint(4, 5)
    while True:  # Second, choose vertical stripes.
      spacing = common.randint(2, 5)
      if col + spacing > width: break
      bcols.extend(range(col, col + spacing))
      col += spacing + common.randint(4, 5)
    while True:  # Keep choosing pixel locations until we land on two colors.
      pixels = common.all_pixels(width, height)
      pixels = common.sample(pixels, common.randint(2, 3))
      pixels = common.remove_diagonal_neighbors(pixels)
      rows, cols = zip(*pixels)
      grid, output = common.grids(width, height, bgcolors[0])
      if draw(grid, output): break

  grid, output = common.grids(width, height, bgcolors[0])
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=19, rows=[5, 8], cols=[4, 1], bgcolors=[8, 2],
               colors=[1, 4], brows=[2, 3, 4, 12, 13, 14, 15],
               bcols=[3, 4, 5, 6]),
      generate(width=14, height=12, rows=[3, 8], cols=[6, 11], bgcolors=[3, 1],
               colors=[8, 2], brows=[5, 6, 7], bcols=[3, 4, 5, 6, 7, 8]),
      generate(width=15, height=15, rows=[5, 8, 10], cols=[7, 4, 12],
               bgcolors=[6, 1], colors=[3, 8], brows=[],
               bcols=[0, 1, 6, 7, 8, 9]),
  ]
  test = [
      generate(width=19, height=17, rows=[0, 4, 12], cols=[10, 6, 14],
               bgcolors=[8, 3], colors=[4, 1], brows=[4, 5, 6, 11, 12, 13, 14],
               bcols=[3, 4, 5, 6, 7, 8]),
  ]
  return {"train": train, "test": test}
