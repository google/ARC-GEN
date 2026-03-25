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
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to use.
  """

  if width is None:
    width, height = common.randint(1, 4), common.randint(1, 4)
    subset = common.random_colors(common.randint(3, 6))
    while True:
      colors = common.choices(subset + [0], width * height)
      good = True
      # Let's avoid a square where they're all the same color.
      for row in range(1, height):
        for col in range(1, width):
          if colors[row * width + col] != colors[row * width + col - 1]:
            continue
          if colors[row * width + col] != colors[(row - 1) * width + col]:
            continue
          if colors[row * width + col] != colors[(row - 1) * width + col - 1]:
            continue
          good = False
      # Let's also make sure no row or column is blank.
      for row in range(height):
        if sum([colors[row * width + col] for col in range(width)]) == 0:
          good = False
      for col in range(width):
        if sum([colors[row * width + col] for row in range(height)]) == 0:
          good = False
      if good: break

  wide, tall = (24 - 2 * width) // width, (24 - 2 * height) // height
  grid, output = common.grid(2 * width + 1, 2 * height + 1), common.grid(26, 26)
  # First, draw the squares themselves.
  for row in range(height):
    for col in range(width):
      color = colors[row * width + col]
      grid[2 * row + 1][2 * col + 1] = color
      r, c = (2 + tall) * row + 2, (2 + wide) * col + 2
      common.rect(output, wide, tall, r, c, color)
  # Second, draw the left-to-right connective tissue.
  taken = common.grid(width, height)
  for row in range(height):
    for col in range(1, width):
      color = colors[row * width + col]
      if color != colors[row * width + col - 1]: continue
      taken[row][col] = taken[row][col - 1] = 1
      r, c = (2 + tall) * row + 2, (2 + wide) * col
      common.rect(output, 2, tall, r, c, color)
  # Third, draw the top-to-bottom connective tissue.
  for col in range(width):
    for row in range(1, height):
      color = colors[row * width + col]
      if color != colors[(row - 1) * width + col]: continue
      if taken[row][col] or taken[row - 1][col]: continue
      r, c = (2 + tall) * row, (2 + wide) * col + 2
      common.rect(output, wide, 2, r, c, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=4, colors=[4, 4, 6, 0, 8, 8, 8, 4]),
      generate(width=3, height=2, colors=[8, 6, 3, 8, 4, 4]),
      generate(width=4, height=4,
               colors=[4, 8, 8, 8, 4, 4, 6, 8, 8, 3, 8, 8, 0, 8, 0, 8]),
      generate(width=1, height=2, colors=[6, 4]),
  ]
  test = [
      generate(width=3, height=3, colors=[6, 3, 4, 8, 1, 7, 8, 7, 7]),
  ]
  return {"train": train, "test": test}
