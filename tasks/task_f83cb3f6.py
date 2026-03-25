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


def generate(width=None, height=None, pos=None, xpose=None, fgcolor=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    pos: The position of the cyan line.
    xpose: Whether the grid is transposed.
    fgcolor: The foreground color.
    colors: The colors of the input grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
      output[i // width][i % width] = 8 if color == 8 else 0
    changed = False
    if xpose:
      for r in range(height):
        if grid[r][pos] not in [0, 8]: return None, None
        if grid[r][pos] != 8: continue
        if sum(grid[r][c] for c in range(pos)):
          output[r][pos - 1] = fgcolor
          changed = True
        if sum(grid[r][c] for c in range(pos + 1, width)):
          output[r][pos + 1] = fgcolor
          changed = True
    else:
      for c in range(width):
        if grid[pos][c] not in [0, 8]: return None, None
        if grid[pos][c] != 8: continue
        if sum(grid[r][c] for r in range(pos)):
          output[pos - 1][c] = fgcolor
          changed = True
        if sum(grid[r][c] for r in range(pos + 1, height)):
          output[pos + 1][c] = fgcolor
          changed = True
    if not changed: return None, None
    return grid, output

  if width is None:
    fgcolor = common.random_color(exclude=[8])
    while True:
      width, height = common.randint(10, 20), common.randint(10, 20)
      pos = height // 2 + common.randint(-1, 1)
      xpose = common.randint(0, 1)
      colors = common.grid(width, height)
      ub = common.randint(9, 19)
      # Choose the sprinkles.
      for row in range(height):
        for col in range(width):
          if common.randint(0, ub): continue
          colors[row][col] = fgcolor
      # Draw the cyan line.
      for c in range(width):
        if common.randint(0, 5): colors[pos][c] = 8
      if xpose:
        colors = common.transpose(colors)
        width, height = height, width
      colors = common.flatten(colors)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, pos=5, xpose=1, fgcolor=1,
               colors=[0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1,
                       1, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 1, 0, 0, 8, 0, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]),
      generate(width=10, height=17, pos=8, xpose=0, fgcolor=5,
               colors=[0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=10, height=15, pos=7, xpose=0, fgcolor=2,
               colors=[0, 0, 2, 0, 0, 2, 0, 0, 0, 0,
                       2, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                       0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
                       2, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       8, 8, 8, 0, 0, 8, 8, 8, 8, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
                       2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 2, 0, 2, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0, 2,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=15, height=10, pos=7, xpose=1, fgcolor=3,
               colors=[0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3,
                       3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 8, 0, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0,
                       3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 3, 0, 0, 0, 0, 3]),
  ]
  return {"train": train, "test": test}
