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


def generate(size=None, angle=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    angle: The angle of the slide.
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(size, size, 7)
    for i, color in enumerate(colors):
      output[i // size][i % size] = grid[i // size][i % size] = color
    # Remove all the red-surrounded pixels.
    num_removed, num_kept = 0, 0
    for row in range(size):
      for col in range(size):
        if grid[row][col] != 8: continue
        neighbors = set()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          color = common.get_pixel(grid, row + dr, col + dc)
          if color in [2, 7]: neighbors.add(color)
        if not neighbors: return None, None
        if 2 in neighbors and 7 in neighbors: return None, None
        if 2 in neighbors:
          output[row][col] = 2
          num_removed += 1
    # Slide all the other pixels down.
    for row in range(size):
      for col in range(size):
        if grid[row][col] != 8 or output[row][col] != 8: continue
        r, c = row, col
        if angle == 0: r -= 1
        if angle == 1: c += 1
        if angle == 2: r += 1
        if angle == 3: c -= 1
        if grid[r][c] == 8: return None, None  # Avoid twins.
        output[r][c] = 8
        num_kept += 1
    if num_removed == 0 or num_kept == 0: return None, None
    return grid, output

  if size is None:
    size, angle = common.randint(7, 14), common.randint(0, 3)
    num_reds = common.randint(size, size * size // 2)
    while True:
      grid = common.grid(size, size, 7)
      # First, draw the red blob.
      reds = [(common.randint(2, size - 3), common.randint(2, size - 3))]
      while len(reds) < num_reds:
        row, col = common.choice(reds)
        grid[row][col] = 2
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          nr, nc = row + dr, col + dc
          if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in reds:
            grid[nr][nc] = 2
            reds.append((nr, nc))
      # Second, draw the pixels.
      for _ in range(common.randint(size // 2, size)):
        grid[common.randint(0, size - 1)][common.randint(0, size - 1)] = 8
      # Third, draw the maroon bar.
      for i in range(size):
        if angle == 0: grid[0][i], grid[1][i] = 9, 7
        if angle == 1: grid[i][size - 1], grid[i][size - 2] = 9, 7
        if angle == 2: grid[size - 1][i], grid[size - 2][i] = 9, 7
        if angle == 3: grid[i][0], grid[i][1] = 9, 7
      # Fourth, draw and make sure it's OK.
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=11, angle=1, colors=[2, 2, 2, 2, 8, 2, 7, 7, 7, 7, 9,
                                         2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 9,
                                         2, 2, 2, 2, 2, 2, 7, 8, 7, 7, 9,
                                         2, 8, 2, 2, 7, 7, 7, 7, 7, 7, 9,
                                         8, 2, 2, 2, 7, 7, 7, 8, 7, 7, 9,
                                         2, 2, 2, 2, 2, 7, 8, 7, 7, 7, 9,
                                         2, 2, 2, 8, 2, 7, 7, 7, 7, 7, 9,
                                         2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 9,
                                         2, 2, 7, 7, 7, 8, 7, 7, 7, 7, 9,
                                         7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 9,
                                         7, 7, 7, 8, 7, 7, 7, 8, 7, 7, 9]),
      generate(size=8, angle=0, colors=[9, 9, 9, 9, 9, 9, 9, 9,
                                        7, 7, 7, 7, 7, 7, 7, 7,
                                        7, 7, 7, 7, 8, 7, 7, 7,
                                        7, 8, 7, 7, 7, 7, 7, 7,
                                        7, 7, 7, 7, 2, 2, 2, 7,
                                        7, 7, 7, 2, 2, 8, 2, 7,
                                        7, 7, 7, 2, 2, 2, 2, 7,
                                        8, 7, 7, 7, 7, 7, 7, 7]),
      generate(size=12, angle=3, colors=[9, 7, 7, 7, 2, 2, 7, 8, 7, 7, 7, 7,
                                         9, 7, 7, 7, 2, 2, 7, 7, 8, 7, 7, 8,
                                         9, 7, 8, 7, 2, 2, 7, 7, 7, 7, 7, 8,
                                         9, 7, 7, 2, 2, 2, 2, 2, 2, 7, 7, 7,
                                         9, 7, 7, 2, 8, 2, 2, 2, 2, 2, 7, 7,
                                         9, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                         9, 7, 7, 7, 2, 2, 2, 8, 2, 2, 8, 2,
                                         9, 7, 7, 7, 2, 2, 2, 2, 2, 2, 2, 2,
                                         9, 7, 7, 7, 7, 7, 2, 2, 2, 7, 7, 7,
                                         9, 7, 7, 8, 7, 7, 7, 7, 7, 8, 7, 7,
                                         9, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7,
                                         9, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 8]),
  ]
  test = [
      generate(size=13, angle=2, colors=[8, 7, 2, 2, 8, 2, 2, 2, 7, 7, 7, 7, 8,
                                         7, 7, 2, 2, 2, 8, 8, 2, 2, 7, 7, 8, 7,
                                         7, 7, 2, 2, 2, 2, 2, 2, 8, 2, 7, 7, 7,
                                         7, 2, 2, 2, 7, 7, 2, 8, 2, 2, 2, 2, 2,
                                         2, 2, 8, 2, 7, 8, 7, 2, 2, 8, 2, 2, 2,
                                         2, 2, 2, 2, 7, 7, 7, 7, 2, 2, 7, 7, 7,
                                         2, 2, 2, 2, 2, 2, 7, 2, 2, 7, 7, 8, 7,
                                         7, 7, 7, 7, 7, 2, 2, 2, 7, 7, 7, 7, 7,
                                         8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                                         7, 8, 7, 8, 7, 7, 8, 7, 7, 8, 8, 8, 8,
                                         7, 7, 7, 7, 7, 8, 7, 8, 7, 7, 7, 7, 7,
                                         7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                                         9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]),
  ]
  return {"train": train, "test": test}
