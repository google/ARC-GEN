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


def generate(width=None, height=None, bgcolor=None, brows=None, bcols=None,
             colors=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bgcolor: The background color of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    pattern: The pattern of the composition.
  """

  def draw():
    if "0" not in pattern: return None, None  # Ensure some background exposed.
    # Ensure that all components are connected.
    for color in colors:
      pixels = []
      for row in range(height):
        for col in range(width):
          if int(pattern[row * width + col]) == color: pixels.append((row, col))
      if not common.connected(pixels): return None, None
    # Ensure that the whole thing is connected.
    pixels = []
    for row in range(height):
      for col in range(width):
        if int(pattern[row * width + col]): pixels.append((row, col))
    if not common.connected(pixels): return None, None
    grid, output = common.grid(16, 16, bgcolor), common.grid(width, height)
    for brow, bcol, color in zip(brows, bcols, colors):
      common.rect(grid, width, height, brow, bcol, 0)
      for row in range(height):
        for col in range(width):
          if int(pattern[row * width + col]) == color:
            grid[brow + row][bcol + col] = color
      for row in range(height):
        for col in range(width):
          output[row][col] = int(pattern[row * width + col])
    return grid, output

  if width is None:
    while True:
      width, height = common.randint(3, 5), common.randint(3, 5)
      if max(width, height) != 3 and min(width, height) != 5: break
    bgcolor = common.random_color()
    colors = common.random_colors(common.randint(2, 4), exclude=[bgcolor])
    while True:
      brows = [common.randint(1, 15 - height) for _ in colors]
      bcols = [common.randint(1, 15 - width) for _ in colors]
      if not common.overlaps(brows, bcols, [width] * len(colors),
                             [height] * len(colors), 2):
        break
    while True:  # Keep going until the problem is legal.
      grid = common.grid(width, height)
      while True:  # Keep going until all colors are used.
        color = common.choice(colors)
        if common.randint(0, 1):
          length = common.randint(2, width)
          pos = common.randint(0, width - length)
          val = common.randint(0, height - 1)
          for c in range(pos, pos + length):
            grid[val][c] = color
        else:
          length = common.randint(2, height)
          pos = common.randint(0, height - length)
          val = common.randint(0, width - 1)
          for r in range(pos, pos + length):
            grid[r][val] = color
        subset = set(common.flatten(grid))
        if 0 in subset: subset.remove(0)
        if len(subset) == len(colors) and common.randint(0, 1): break
      pattern = "".join(map(str, common.flatten(grid)))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, bgcolor=8, brows=[1, 2, 8, 12],
               bcols=[1, 9, 3, 9], colors=[1, 3, 2, 4], pattern="003311240224"),
      generate(width=4, height=4, bgcolor=1, brows=[1, 2, 10], bcols=[1, 10, 5],
               colors=[2, 3, 4], pattern="4444330033000220"),
      generate(width=5, height=4, bgcolor=9, brows=[1, 8, 2, 6], bcols=[2, 6],
               colors=[1, 2], pattern="01000112200112000020"),
  ]
  test = [
      generate(width=3, height=5, bgcolor=1, brows=[1, 1, 8, 9],
               bcols=[1, 8, 3, 11], colors=[2, 3, 4, 6],
               pattern="023223444640660"),
  ]
  return {"train": train, "test": test}
