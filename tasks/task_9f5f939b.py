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


def generate(size=None, rows=None, cols=None, cdirs=None, expected=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the lines.
    cols: The columns of the lines.
    cdirs: The directions of the lines.
    expected: The expected number of stars.
  """

  def draw():
    grid, output = common.grids(size, size, 8)
    def put(coords, value):
      # First, check that each coord is clear, and has no blue neighbors.
      for row, col in coords:
        if output[row][col] != 8: return False
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
          if common.get_pixel(output, row + dr, col + dc) == 1: return False
      # Second, draw the coords.
      for row, col in coords:
        output[row][col] = grid[row][col] = value
      return True
    # Draw all the blue lines.
    for row, col, cdir in zip(rows, cols, cdirs):
      if not put([(row, col), (row + cdir, col + 1 - cdir)], 1):
        return None, None
    # Now, find the stars and draw them.
    num_stars = 0
    for row in range(3, size - 3):
      for col in range(3, size - 3):
        good = True
        for i in range(2, 4):
          if grid[row - i][col] != 1: good = False
          if grid[row + i][col] != 1: good = False
          if grid[row][col - i] != 1: good = False
          if grid[row][col + i] != 1: good = False
        if good:
          if output[row][col] != 8: return None, None
          output[row][col] = 4
          num_stars += 1
    if num_stars != expected: return None, None  # ensure no accidental stars
    return grid, output

  if size is None:
    size = 4 * common.randint(2, 5)
    min_stars, max_stars = 1, 1
    if size == 16: min_stars, max_stars = 1, 2
    if size == 20: min_stars, max_stars = 3, 4
    expected = common.randint(min_stars, max_stars)
    debris = 1
    if size == 12: debris = 3
    if size == 16: debris = 6
    if size == 20: debris = 20
    while True:
      rows, cols, cdirs = [], [], []
      for _ in range(expected):
        row = common.randint(3, size - 4)
        col = common.randint(3, size - 4)
        rows.extend([row - 3, row, row, row + 2])
        cols.extend([col, col - 3, col + 2, col])
        cdirs.extend([1, 0, 0, 1])
      grid, _ = draw()
      if grid: break
    for _ in range(debris):
      while True:  # Keep trying to add a single debris until it succeeds.
        rows.append(common.randint(0, size - 2))
        cols.append(common.randint(0, size - 2))
        cdirs.append(common.randint(0, 1))
        grid, _ = draw()
        if grid: break
        rows.pop()
        cols.pop()
        cdirs.pop()

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, rows=[2, 2, 4, 5, 5, 7, 8, 11, 12, 12],
               cols=[4, 10, 12, 1, 6, 4, 8, 11, 2, 9],
               cdirs=[1, 0, 1, 0, 0, 1, 1, 0, 1, 0], expected=1),
      generate(size=8, rows=[1, 2, 4, 4, 6], cols=[3, 6, 0, 5, 3],
               cdirs=[1, 0, 0, 0, 1], expected=1),
      generate(size=16, rows=[1, 2, 5, 5, 5, 7, 7, 8, 10, 11, 11, 12, 12, 13, 14],
               cols=[5, 10, 2, 7, 12, 5, 10, 12, 3, 9, 14, 0, 5, 12, 3],
               cdirs=[1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1], expected=2),
  ]
  test = [
      generate(size=20,
               rows=[0, 0, 0, 1, 2, 2, 2, 3, 4, 4, 4, 6, 6, 6, 6, 6, 8, 9, 9, 9, 11, 11, 11, 11, 12, 13, 13, 14, 14, 15, 15, 16, 16, 16, 17, 18, 18, 18, 19],
               cols=[0, 7, 16, 14, 4, 10, 18, 3, 7, 11, 16, 0, 5, 8, 14, 19, 3, 5, 10, 16, 3, 8, 10, 14, 18, 0, 5, 7, 12, 3, 15, 6, 10, 14, 0, 3, 8, 18, 11],
               cdirs=[0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0], expected=4),
  ]
  return {"train": train, "test": test}
