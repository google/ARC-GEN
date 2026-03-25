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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    colors: a list of digits representing the colors to be used
  """
  def find_most(bitmap):
    most, rows, cols, wides, talls = -1, [], [], [], []
    for r2 in range(height):
      for r1 in range(r2):
        for c2 in range(width):
          for c1 in range(c2):
            alive = sum([sum(bitmap[r][c1:c2+1]) for r in range(r1, r2+1)])
            if alive: continue
            size = (r2 - r1 + 1) * (c2 - c1 + 1)
            if size < most: continue
            if size > most:
              most, rows, cols, wides, talls = size, [], [], [], []
            rows.append(r1)
            cols.append(c1)
            wides.append(c2 - c1 + 1)
            talls.append(r2 - r1 + 1)
    return rows, cols, wides, talls

  if width is None:
    width, height = common.randint(20, 30), common.randint(2, 5)
    while True:
      # First add the random static.
      grid = common.grid(width, height)
      pixels = common.random_pixels(width, height)
      for r, c in pixels:
        grid[r][c] = common.blue() if common.randint(0, 100) else common.gray()
      # Then remove a small cutout.
      wide, tall = common.randint(2, 5), common.randint(2, height)
      row = common.randint(0, height - tall)
      col = common.randint(0, width - wide)
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          grid[r][c] = common.black()
      # Finally, make sure it's unique (no more than one big cutout)
      rows, _, _, _ = find_most(grid)
      if len(rows) == 1: break
    colors = []
    for r in range(height):
      for c in range(width):
        colors.append(grid[r][c])

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c] = colors[r * width + c]
  rows, cols, wides, talls = find_most(grid)
  for r in range(rows[0], rows[0] + talls[0]):
    for c in range(cols[0], cols[0] + wides[0]):
      output[r][c] = common.pink()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=3,
               colors=[5, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                       0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1,
                       1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1,
                       1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0,
                       0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]),
      generate(width=20, height=4,
               colors=[1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0,
                       1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1,
                       1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1,
                       1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,
                       1, 1, 1, 1]),
      generate(width=20, height=2,
               colors=[1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0,
                       0, 0]),
      generate(width=20, height=4,
               colors=[0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
                       1, 0, 0, 1]),
  ]
  test = [
      generate(width=24, height=4,
               colors=[0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                       1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1,
                       0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
                       1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1,
                       0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0,
                       1]),
  ]
  return {"train": train, "test": test}
