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


def generate(width=None, height=None, bgcolor=None, fgcolor=None, length=None,
             spacing=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bgcolor: The background color of the grid.
    fgcolor: The foreground color of the grid.
    length: The length of the squares.
    spacing: The spacing between the squares.
    colors: The colors of the static.
  """

  if width is None:
    fgcolor = common.random_color(exclude=[6])
    bgcolor = common.random_color(exclude=[6, fgcolor])
    length = common.randint(1, 2)
    spacing = length + common.randint(1, 2)
    while True:
      wide, tall = common.randint(4, 10), common.randint(4, 10)
      width, height = wide * spacing, tall * spacing
      if spacing == length + 1: width, height = width + 1, height + 1
      if width >= 10 and height >= 10 and width <= 20 and height <= 20: break
    colors = [0 if common.randint(0, 9) else 6 for _ in range(width * height)]

  grid, output = common.grids(width, height, bgcolor)
  for row in range(1, height, spacing):
    for col in range(1, width, spacing):
      common.rect(grid, length, length, row, col, fgcolor)
      common.rect(output, length, length, row, col, fgcolor)
  for i, color in enumerate(colors):
    if color: grid[i // width][i % width] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=12, bgcolor=7, fgcolor=8, length=1, spacing=3,
               colors=[0, 0, 6, 0, 0, 6, 0, 6, 0, 0, 0, 6,
                       0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0,
                       0, 6, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0,
                       0, 6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 6,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6,
                       0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 0]),
      generate(width=19, height=15, bgcolor=8, fgcolor=4, length=1, spacing=2,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 6, 6, 6, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0,
                       6, 0, 0, 6, 0, 6, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 6, 0, 0,
                       0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
                       0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 6, 0, 6,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0,
                       0, 0, 0, 0, 6, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 6, 0, 0, 0, 0, 6, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 6, 0, 6, 6, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 0, 6, 0, 6, 0, 0, 0, 0, 0,
                       0, 0, 0, 6, 0, 6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 0,
                       0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=16, height=16, bgcolor=3, fgcolor=1, length=2, spacing=3,
               colors=[0, 6, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       6, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 0,
                       6, 6, 0, 0, 6, 6, 6, 0, 6, 0, 0, 0, 6, 0, 6, 0,
                       0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 6,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 6, 0, 0, 0,
                       0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
                       6, 6, 0, 0, 6, 6, 0, 6, 0, 0, 6, 6, 0, 0, 0, 6,
                       6, 0, 0, 0, 6, 6, 0, 6, 0, 0, 0, 6, 0, 6, 0, 6,
                       0, 0, 6, 0, 6, 0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 6,
                       0, 0, 0, 0, 0, 6, 0, 0, 6, 0, 6, 0, 0, 0, 0, 6,
                       6, 6, 0, 6, 0, 0, 0, 6, 0, 0, 6, 6, 0, 6, 0, 6,
                       0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 0, 6, 6, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
