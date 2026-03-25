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


def generate(rows=None, cols=None, colors=None, rdiffs=None, cdiffs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The cols of the pixels.
    colors: The colors of the pixels.
    rdiffs: The differences of the rows.
    cdiffs: The differences of the cols.
  """

  def draw():
    # We want there to be lots of spacing between the pixels, at least initially
    if common.overlaps(rows, cols, [2] * len(rows), [2] * len(cols)):
      return None, None
    # We also want to make sure that only one of each color moves.
    colors_moved = [color for color, rdiff, cdiff in zip(colors, rdiffs, cdiffs) if rdiff != 0 or cdiff != 0]
    if len(colors_moved) != len(set(colors_moved)): return None, None
    # Now we can draw.
    grid, output = common.grid(21, 10), common.grid(10, 10)
    for row in range(10):
      grid[row][10] = 5
    for row, col, color, rdiff, cdiff in zip(rows, cols, colors, rdiffs, cdiffs):
      # First, check that we're in bounds.
      if row < 0 or row >= 10 or col < 0 or col >= 10: return None, None
      if row + rdiff < 0 or row + rdiff >= 10 or col + cdiff < 0 or col + cdiff >= 10:
        return None, None
      # Second, check that we're not drawing over anything.
      if grid[row][col] != 0: return None, None
      if grid[row + rdiff][col + cdiff] != 0: return None, None
      if output[row][col] != 0: return None, None
      if output[row + rdiff][col + cdiff] != 0: return None, None
      # Third, draw the pixels.
      grid[row][col] = color
      grid[row + rdiff][col + cdiff + 11] = color
      if rdiff == 0 and cdiff == 0:
        output[row][col] = color
      else:
        output[row][col] = 2
        output[row + rdiff][col + cdiff] = 1
    return grid, output

  if rows is None:
    subset = common.random_colors(common.randint(2, 3), exclude=[1, 2, 5])
    pixels = common.randint(5, 10)
    to_move = common.sample(list(range(pixels)), common.randint(1, 2))
    while True:
      colors = common.choices(subset, pixels)
      if len(set(colors)) != len(subset): continue
      cdiffs, rdiffs = [0] * pixels, [0] * pixels
      for i in to_move:
        while True:  # Keep trying until there's a diff, but not too far away.
          cdiffs[i] = common.randint(-2, 2)
          rdiffs[i] = common.randint(-2, 2)
          if cdiffs[i] == 0 and rdiffs[i] == 0: continue
          if abs(cdiffs[i]) == 2 and abs(rdiffs[i]) == 2: continue
          break
      rows = [common.randint(0, 9) for _ in range(pixels)]
      cols = [common.randint(0, 9) for _ in range(pixels)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 3, 3, 4, 5, 7, 8], cols=[3, 6, 1, 5, 7, 1, 3, 7],
               colors=[4, 8, 9, 8, 4, 4, 8, 9],
               rdiffs=[0, 0, 0, 0, 0, 0, 0, -1],
               cdiffs=[0, 0, 0, -1, 0, 0, 0, -1]),
      generate(rows=[1, 2, 2, 4, 5, 8, 8], cols=[8, 2, 5, 3, 6, 1, 7],
               colors=[6, 3, 3, 6, 3, 3, 6], rdiffs=[0, 0, 0, 0, 1, 0, 0],
               cdiffs=[0, 0, 0, 0, 0, 0, 0]),
      generate(rows=[1, 2, 3, 3, 4, 5, 8, 8], cols=[7, 3, 1, 9, 5, 3, 3, 7],
               colors=[8, 8, 3, 3, 3, 6, 8, 6],
               rdiffs=[0, 0, 0, 0, -1, 0, 0, -2],
               cdiffs=[0, 0, 0, 0, 1, 0, 0, 0]),
  ]
  test = [
      generate(rows=[0, 1, 2, 2, 4, 4, 6, 8, 8, 9],
               cols=[4, 1, 3, 7, 3, 6, 1, 4, 7, 1],
               colors=[4, 9, 4, 9, 9, 7, 4, 7, 4, 9],
               rdiffs=[1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
               cdiffs=[2, 0, 0, 0, 0, -1, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
