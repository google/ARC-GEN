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


def generate(width=None, height=None, static=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    static: the color of the static
    colors: a list of colors to be used in the input grid
  """
  if width is None:
    height = common.randint(15, 20)
    static = common.random_color(exclude=[common.red(), common.yellow()])
    width = height + common.randint(-1, 1)
    # First, create random static.
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)
    grid = common.grid(width, height)
    for r, c in zip(rows, cols):
      grid[r][c] = static
    # Second, create a few rectangles underneath.
    num_boxes, rows, cols, wides, talls = common.randint(2, 4), [], [], [], []
    while len(rows) < num_boxes:
      w, t = common.randint(2, 7), common.randint(2, 3)
      r, c = common.randint(0, height - t), common.randint(0, width - w)
      if common.overlaps(rows + [r], cols + [c], wides + [w], talls + [t], 2):
        continue
      legal = True  # Check to make sure that each row / col is visible.
      for row in range(r, r + t):
        visible = False
        for col in range(c, c + w):
          if not grid[row][col]: visible = True
        if not visible: legal = False
      for col in range(c, c + w):
        visible = False
        for row in range(r, r + t):
          if not grid[row][col]: visible = True
        if not visible: legal = False
      if not legal: continue
      rows.append(r)
      cols.append(c)
      wides.append(w)
      talls.append(t)
      for row in range(r, r + t):
        for col in range(c, c + w):
          grid[row][col] = common.yellow() if grid[row][col] else common.red()
    # Finally, flatten the colors into a list.
    colors = []
    for r in range(height):
      for c in range(width):
        colors.append(grid[r][c])

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      color = colors[r * width + c]
      output[r][c] = color
      grid[r][c] = color if color != common.yellow() else static
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=17, static=1,
               colors=[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1,
                       1, 2, 4, 4, 4, 4, 4, 4, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1,
                       4, 2, 4, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 2,
                       4, 2, 2, 2, 2, 2, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0,
                       1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1,
                       0, 0, 0, 1, 0, 0, 0, 4, 2, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 2, 4, 2, 4,
                       2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4,
                       0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 4, 2, 4, 2, 2, 0,
                       0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
                       1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
                       0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                       1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
                       0, 1]),
      generate(width=16, height=15, static=8,
               colors=[8, 0, 0, 0, 0, 8, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0, 8, 0,
                       0, 0, 0, 0, 0, 0, 8, 0, 8, 0, 8, 0, 0, 0, 0, 8, 8, 8, 0,
                       8, 8, 8, 8, 8, 8, 0, 8, 0, 8, 0, 0, 8, 0, 8, 0, 0, 0, 0,
                       8, 0, 4, 4, 2, 8, 0, 0, 0, 2, 4, 2, 2, 2, 8, 0, 0, 0, 2,
                       4, 2, 8, 0, 8, 0, 2, 4, 2, 4, 4, 8, 0, 0, 0, 8, 0, 0, 8,
                       8, 8, 0, 0, 8, 8, 0, 8, 8, 8, 8, 0, 8, 8, 0, 0, 0, 8, 0,
                       8, 0, 8, 0, 8, 0, 8, 8, 0, 8, 8, 8, 0, 8, 8, 0, 0, 0, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 4, 4, 2, 4, 8, 8,
                       0, 8, 0, 0, 0, 8, 8, 8, 8, 0, 2, 4, 4, 2, 8, 8, 0, 8, 0,
                       0, 8, 8, 0, 8, 0, 8, 0, 0, 0, 8, 8, 0, 0, 2, 4, 4, 0, 8,
                       8, 8, 8, 0, 0, 8, 8, 8, 8, 0, 0, 2, 4, 2, 0, 0, 0, 8, 0,
                       8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8, 0,
                       8, 0, 8, 0, 0, 0, 8, 8, 8, 8, 8, 8]),
      generate(width=14, height=15, static=3,
               colors=[3, 3, 0, 0, 0, 0, 0, 3, 0, 3, 3, 0, 0, 0, 0, 0, 3, 0, 0,
                       3, 3, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 3,
                       0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 3, 0,
                       0, 0, 2, 2, 2, 2, 4, 0, 0, 0, 3, 0, 3, 0, 3, 3, 2, 2, 4,
                       4, 2, 0, 0, 0, 3, 3, 0, 0, 3, 0, 2, 2, 2, 4, 2, 0, 0, 3,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 0, 0, 0, 0, 3, 0, 0,
                       3, 3, 0, 3, 3, 0, 3, 3, 0, 0, 3, 3, 3, 3, 4, 2, 0, 3, 3,
                       0, 0, 0, 3, 0, 3, 0, 0, 3, 2, 4, 0, 0, 0, 3, 3, 0, 0, 0,
                       3, 0, 0, 3, 3, 0, 3, 3, 0, 0, 3, 3, 0, 3, 0, 3, 0, 0, 3,
                       0, 3, 3, 0, 0, 3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 3, 0, 3, 0,
                       3, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 3, 3, 0, 3,
                       3]),
  ]
  test = [
      generate(width=18, height=17, static=9,
               colors=[0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9, 0, 9,
                       2, 4, 2, 2, 4, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 2,
                       2, 4, 4, 2, 0, 0, 9, 9, 9, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 9, 9, 0,
                       0, 0, 9, 0, 9, 9, 0, 9, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0,
                       9, 2, 4, 2, 2, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                       2, 2, 2, 2, 9, 0, 9, 9, 0, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0,
                       0, 9, 0, 9, 9, 0, 9, 9, 9, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9,
                       9, 9, 9, 9, 0, 9, 0, 0, 0, 0, 9, 9, 0, 9, 0, 9, 0, 9, 9,
                       0, 0, 9, 9, 0, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 4, 2, 9, 0,
                       0, 9, 0, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 9, 2, 4, 9, 9, 0,
                       0, 0, 9, 9, 9, 0, 9, 9, 0, 9, 9, 0, 9, 9, 9, 0, 0, 9, 0,
                       0, 0, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 2, 2,
                       4, 2, 2, 4, 0, 0, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 2, 4, 2,
                       4, 4, 2, 9, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 0, 2, 2, 4, 2,
                       2, 4, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 9, 9,
                       9, 0]),
  ]
  return {"train": train, "test": test}
