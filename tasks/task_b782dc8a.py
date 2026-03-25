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
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to be used in the grid.
  """
  if width is None:
    width, height = common.randint(10, 25), common.randint(10, 25)
    grid = common.grid(width, height, common.cyan())
    rmod, cmod = common.randint(0, 1), common.randint(0, 1)
    while True:
      # Find some point in the grid to start clearing a path.
      rows, cols = [], []
      for r in range(height):
        for c in range(width):
          if r % 2 != rmod or c % 2 != cmod: continue
          viable = True
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              if not common.get_pixel(grid, r + dr, c + dc): viable = False
          if not viable: continue
          rows.append(r)
          cols.append(c)
      if not rows: break  # No viable points!
      # Start path clearing from a random viable point.
      idx = common.randint(0, len(rows)) - 1
      row, col = rows[idx], cols[idx]
      queue = [(row, col)]
      grid[row][col] = common.black()
      while queue:
        i = common.randint(0, len(queue) - 1)
        r, c = queue[i]
        del queue[i]
        if not common.randint(0, 2): continue  # Sometimes we trim paths.
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
          if common.get_pixel(grid, r + dr, c + dc) in [0, -1]: continue
          if common.get_pixel(grid, r + 2 * dr, c + 2 * dc) in [0, -1]: continue
          grid[r + dr][c + dc] = grid[r + 2 * dr][c + 2 * dc] = common.black()
          queue.append((r + 2 * dr, c + 2 * dc))
    # Find some spot in the grid with a couple empty places, and draw colors.
    while True:
      row, col = common.randint(1, height - 2), common.randint(1, width - 2)
      if (not grid[row][col]) and (not grid[row + 1][col]): break
    pair = common.random_colors(2, exclude=[common.cyan()])
    grid[row][col] = pair[0]
    for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
      if grid[row + dr][col + dc] == 0: grid[row + dr][col + dc] = pair[1]
    colors = []
    for row in grid:
      colors.extend(row)

  grid, output = common.grids(width, height)
  pair, queue = [None, None], []
  for r in range(height):
    for c in range(width):
      if colors[r * width + c] in [common.black(), common.cyan()]:
        grid[r][c] = output[r][c] = colors[r * width + c]
        continue
      grid[r][c] = colors[r * width + c]
      pair[(r + c) % 2] = colors[r * width + c]
      queue.append((r, c))
  while queue:
    r, c = queue.pop()
    if r in [-1, height] or c in [-1, width] or output[r][c]: continue
    for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
      queue.append((r + dr, c + dc))
    output[r][c] = pair[(r + c) % 2]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=24, height=11,
               colors=[8, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8,
                       0, 8, 8, 8, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 8, 0, 0,
                       0, 8, 0, 8, 0, 0, 8, 0, 8, 0, 8, 8, 8, 0, 8, 0, 8, 8, 8,
                       8, 0, 8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 0, 8, 0, 8, 0, 0, 0,
                       8, 0, 8, 0, 0, 8, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0, 8,
                       0, 8, 0, 8, 8, 8, 0, 8, 8, 0, 8, 0, 8, 8, 8, 0, 8, 8, 0,
                       8, 8, 8, 8, 8, 0, 8, 0, 8, 0, 0, 0, 0, 8, 0, 8, 0, 8, 0,
                       0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8,
                       0, 8, 0, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 0, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 3, 2, 3, 0, 0, 0,
                       8, 0, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8,
                       3, 8, 8, 8, 0, 8, 0, 0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 0, 8,
                       0, 0, 0, 0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 8, 8, 8, 0, 8, 8,
                       8, 0, 8, 8, 8, 0, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0]),
      generate(width=14, height=13,
               colors=[0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8,
                       8, 0, 8, 0, 8, 8, 8, 0, 8, 0, 8, 0, 0, 0, 8, 0, 8, 0, 8,
                       0, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 0, 8, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8, 8,
                       0, 8, 0, 0, 0, 8, 0, 8, 8, 0, 0, 0, 0, 8, 0, 8, 8, 8, 0,
                       8, 0, 8, 8, 8, 8, 8, 0, 8, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0,
                       0, 8, 1, 8, 8, 8, 8, 8, 0, 8, 8, 0, 8, 8, 0, 8, 4, 1, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 8, 0, 8, 1, 8, 8, 8, 8, 8, 8, 8,
                       8, 0, 0, 8, 8, 8, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(width=15, height=15,
               colors=[8, 8, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 8,
                       8, 8, 8, 4, 8, 8, 8, 8, 8, 8, 8, 0, 8, 0, 0, 0, 0, 4, 3,
                       8, 0, 0, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 0,
                       8, 8, 8, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 8, 0, 0, 8,
                       8, 8, 8, 8, 0, 8, 8, 8, 0, 8, 0, 8, 0, 8, 0, 0, 0, 0, 8,
                       0, 0, 0, 8, 0, 8, 0, 8, 0, 8, 8, 8, 8, 0, 8, 8, 8, 0, 8,
                       0, 8, 0, 8, 8, 8, 0, 0, 8, 0, 0, 0, 8, 0, 8, 0, 8, 0, 0,
                       0, 0, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 8, 0, 8, 8, 0,
                       0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 8, 8, 8, 8, 0, 8, 0,
                       8, 8, 8, 8, 8, 8, 8, 0, 8, 0, 0, 8, 0, 8, 0, 8, 0, 0, 0,
                       0, 0, 0, 0, 8, 8, 0, 8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 8, 8,
                       8, 8, 0, 0, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
