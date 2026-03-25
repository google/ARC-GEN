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


def generate(wide=None, tall=None, bgcolor=None, cdirs=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: The width of the grid.
    tall: The height of the grid.
    bgcolor: The background color of the grid.
    cdirs: The directions of the boxes.
    colors: The colors of the boxes.
  """

  if colors is None:
    wide, tall = common.randint(1, 3), common.randint(1, 3)
    bgcolor = common.random_color(exclude=[4])
    cdirs = [common.randint(0, 2) for _ in range(wide * tall)]
    colors = []
    for cdir in cdirs:
      if cdir in [0, 1]:
        colors.extend(common.random_colors(4, exclude=[4, bgcolor]))
      else:
        pair = common.random_colors(2, exclude=[4, bgcolor])
        hues = [pair[0], pair[1], pair[1], pair[1]]
        colors.extend(common.shuffle(hues))

  width, height = 10 * wide - 1, 10 * tall - 1
  grid, output = common.grids(width, height)
  # Draw the mega grid.
  for r in range(height):
    for c in range(9, width, 10):
      output[r][c] = grid[r][c] = bgcolor
  for r in range(9, height, 10):
    for c in range(width):
      output[r][c] = grid[r][c] = bgcolor
  # Draw each box's contents.
  for row in range(tall):
    for col in range(wide):
      cdir = cdirs[row * wide + col]
      hues = colors[4 * (row * wide + col):4 * (row * wide + col + 1)]
      if cdir != 2:
        for i in range(9):
          r, c = row * 10 + (i if cdir else 4), col * 10 + (4 if cdir else i)
          output[r][c] = grid[r][c] = 4
      for x in range(2):
        for y in range(2):
          r, c = row * 10 + 4 * x + 1, col * 10 + 4 * y + 1
          common.rect(grid, 3, 3, r, c, hues[x * 2 + y])
          if cdir == 0:
            common.rect(output, 3, 3, r, c, hues[(1 - x) * 2 + y])
          if cdir == 1:
            common.rect(output, 3, 3, r, c, hues[x * 2 + 1 - y])
          if cdir == 2:
            hue = sorted([(hues.count(h), h) for h in set(hues)])[0][1]
            common.rect(output, 3, 3, r, c, hue)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=1, tall=1, bgcolor=5, cdirs=[1], colors=[2, 1, 1, 8]),
      generate(wide=1, tall=2, bgcolor=7, cdirs=[2, 0],
               colors=[1, 6, 1, 1, 3, 9, 2, 8]),
      generate(wide=1, tall=1, bgcolor=5, cdirs=[2], colors=[1, 1, 8, 1]),
      generate(wide=2, tall=2, bgcolor=5, cdirs=[2, 1, 0, 2],
               colors=[1, 4, 1, 1, 2, 8, 3, 1, 1, 8, 6, 3, 1, 1, 2, 1]),
  ]
  test = [
      generate(wide=3, tall=2, bgcolor=5, cdirs=[1, 2, 2, 2, 2, 0],
               colors=[1, 3, 3, 5, 6, 1, 1, 1, 1, 1, 4, 1, 2, 1, 1, 1, 1, 1, 1, 8, 8, 5, 1, 6]),
      generate(wide=3, tall=3, bgcolor=9, cdirs=[2, 1, 2, 0, 2, 0, 1, 0, 2],
               colors=[3, 1, 1, 1, 8, 1, 6, 3, 1, 7, 1, 1, 8, 3, 2, 1, 5, 1, 1, 1, 2, 7, 8, 1, 6, 6, 3, 1, 7, 1, 2, 8, 1, 2, 1, 1]),
  ]
  return {"train": train, "test": test}
