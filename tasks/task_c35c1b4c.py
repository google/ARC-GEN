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


def generate(fgcolor=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    fgcolor: The foreground color.
    colors: A list of colors to use.
  """

  if fgcolor is None:
    num_pixels = common.randint(18, 24)
    subset = common.random_colors(3)
    fgcolor = subset.pop()
    grid = common.grid(10, 10)
    for row in range(10):
      for col in range(10):
        grid[row][col] = common.choice(subset + [0])
    grid[4][4] = fgcolor
    queue = [(4, 4)]
    while True:
      idx = common.randint(0, len(queue) - 1)
      r, c = queue.pop(idx)
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 1 <= nr < 9 and 0 <= nc < 5 and grid[nr][nc] != fgcolor:
          grid[nr][nc] = fgcolor
          if common.randint(0, 1): grid[nr][9 - nc] = fgcolor
          queue.append((nr, nc))
          num_pixels -= 1
      if num_pixels <= 0: break
    colors = common.flatten(grid)

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    output[i // 10][i % 10] = grid[i // 10][i % 10] = color
  for r in range(10):
    for c in range(5):
      if output[r][c] == fgcolor: output[r][9 - c] = fgcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(fgcolor=3, colors=[9, 0, 0, 0, 0, 7, 7, 0, 9, 0,
                                  0, 0, 9, 0, 0, 0, 9, 9, 9, 0,
                                  7, 7, 0, 3, 3, 3, 3, 7, 9, 7,
                                  0, 3, 7, 3, 3, 3, 3, 9, 3, 7,
                                  0, 3, 9, 3, 3, 0, 0, 0, 3, 9,
                                  9, 3, 3, 3, 3, 0, 0, 9, 3, 0,
                                  3, 3, 3, 3, 3, 9, 0, 0, 3, 7,
                                  3, 3, 3, 3, 3, 0, 9, 9, 3, 0,
                                  0, 9, 0, 3, 3, 3, 9, 9, 9, 9,
                                  7, 9, 7, 9, 0, 0, 7, 7, 0, 0]),
      generate(fgcolor=1, colors=[6, 6, 8, 8, 8, 0, 8, 0, 6, 0,
                                  0, 8, 0, 0, 6, 6, 6, 6, 8, 0,
                                  6, 6, 0, 1, 1, 1, 1, 0, 6, 6,
                                  0, 0, 1, 1, 1, 1, 1, 1, 0, 0,
                                  8, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                                  6, 1, 1, 1, 1, 1, 1, 1, 6, 0,
                                  6, 1, 1, 1, 1, 1, 1, 1, 6, 8,
                                  0, 8, 1, 1, 1, 8, 6, 8, 0, 0,
                                  6, 8, 6, 0, 6, 0, 8, 0, 6, 8,
                                  8, 6, 0, 6, 0, 6, 6, 8, 0, 8]),
      generate(fgcolor=2, colors=[1, 1, 0, 1, 1, 0, 0, 0, 4, 1,
                                  4, 4, 0, 4, 2, 2, 1, 4, 4, 4,
                                  4, 0, 2, 2, 2, 2, 2, 2, 1, 0,
                                  0, 4, 2, 2, 2, 0, 0, 1, 1, 0,
                                  0, 0, 1, 2, 2, 2, 1, 0, 1, 0,
                                  0, 4, 0, 2, 2, 0, 2, 0, 0, 0,
                                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                  4, 1, 4, 1, 2, 2, 4, 4, 1, 4,
                                  0, 4, 4, 4, 2, 1, 1, 4, 4, 1,
                                  4, 0, 4, 4, 0, 4, 1, 1, 4, 0]),
  ]
  test = [
      generate(fgcolor=9, colors=[0, 0, 6, 6, 6, 6, 0, 6, 6, 0,
                                  2, 6, 0, 6, 9, 0, 6, 0, 2, 6,
                                  2, 6, 6, 9, 9, 9, 9, 0, 6, 6,
                                  2, 0, 0, 9, 9, 0, 9, 6, 0, 2,
                                  9, 9, 9, 9, 9, 9, 6, 0, 0, 0,
                                  9, 9, 9, 9, 9, 9, 9, 9, 0, 0,
                                  0, 0, 9, 9, 9, 9, 6, 6, 0, 0,
                                  2, 9, 9, 9, 9, 9, 9, 6, 2, 6,
                                  0, 0, 2, 9, 0, 6, 9, 0, 2, 6,
                                  6, 0, 0, 2, 0, 6, 0, 6, 6, 2]),
  ]
  return {"train": train, "test": test}
