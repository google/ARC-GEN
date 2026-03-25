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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    colors: The colors to use.
  """

  if width is None:
    width, height = common.randint(9, 30), 2 * common.randint(1, 5) + 1
    color = common.random_color(exclude=[8])
    while True:
      wide, tall = common.randint(3, width // 2), common.randint(3, height)
      pixels = []
      for row in range(tall):
        for col in range(wide):
          if common.randint(0, 1): pixels.append((row, col))
      if not pixels or not common.diagonally_connected(pixels): continue
      if len(pixels) % 2 == width % 2 and len(pixels) <= width: break
    grid = common.grid(width, height, 8)
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    for row in range(height):
      for col in range(width):
        if (row, col) in pixels: grid[brow + row][bcol + col] = color
    colors = common.flatten(grid)

  grid, output = common.grids(width, height, 8)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
  hues = set(colors)
  hues.remove(8)
  hue = hues.pop()
  count = colors.count(hue)
  for i in range(count):
    output[height // 2][(width - count) // 2 + i] = hue
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=7,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 9, 9, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 9, 9, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 9, 9, 9, 8, 8, 8,
                       8, 8, 8, 8, 9, 8, 9, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(width=10, height=5,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 3, 8, 8, 8,
                       8, 8, 8, 8, 3, 3, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 3, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
      generate(width=15, height=9,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 8, 8,
                       8, 8, 8, 8, 8, 2, 8, 8, 2, 2, 8, 8, 2, 8, 8,
                       8, 8, 8, 8, 8, 8, 2, 8, 2, 2, 2, 8, 2, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 2, 8, 8, 8, 2, 2, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(width=28, height=11,
               colors=[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 5, 8, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
