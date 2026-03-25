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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, lrow=None, lcol=None, lspacing=None, lcolors=None,
             lcorners=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The width of the grid of squares.
    tall: The height of the grid of squares.
    brow: The row of the square grid.
    bcol: The column of the square grid.
    lrow: The row of the legend.
    lcol: The column of the legend.
    lspacing: The spacing between the legend items.
    lcolors: The colors of the legend items.
    lcorners: The corners of the legend items.
    colors: The colors of the squares in the square grid.
  """

  if width is None:
    width, height = common.randint(16, 20), common.randint(16, 20)
    wide = common.randint(4, 5)
    tall = common.randint(3, 3 if height < 19 else 4)
    lcolors = common.sample([2, 3, 4, 7, 8], common.randint(3, 4))
    lcorners = common.sample([-1, 0, 1, 2, 3], len(lcolors))
    lspacing = common.randint(1, 1 if len(lcolors) == 4 and width < 18 else 2)
    lrow = common.randint(0, 1)
    lcol = common.randint(0, width - (lspacing + 3) * len(lcolors) + 1)
    brow, bcol = 7, common.randint(1, width - 3 * wide)
    while True:
      colors = common.choices(lcolors + [-1], wide * tall)
      if len(set(colors)) == len(lcolors) + 1: break

  out_width, out_height = wide * 3 - 1, tall * 3 - 1
  grid, output = common.grid(width, height), common.grid(out_width, out_height)
  # Draw the input grid.
  for row in range(tall):
    for col in range(wide):
      common.rect(grid, 2, 2, brow + row * 3, bcol + col * 3, 5)
      color = colors[row * wide + col]
      if color != -1: grid[brow + row * 3 + 1][bcol + col * 3 + 1] = color
  # Draw the input legend.
  color_to_corner = {}
  for i, (lcolor, lcorner) in enumerate(zip(lcolors, lcorners)):
    color_to_corner[lcolor] = lcorner
    grid[lrow][lcol + i * (lspacing + 3)] = lcolor
    for r in range(2):
      for c in range(2):
        if r * 2 + c == lcorner: continue
        grid[lrow + r + 1][lcol + i * (lspacing + 3) + 1 + c] = 1
  # Draw the output.
  for row in range(tall):
    for col in range(wide):
      color = colors[row * wide + col]
      if color == -1: continue
      for r in range(2):
        for c in range(2):
          if r * 2 + c == color_to_corner[color]: continue
          output[row * 3 + r][col * 3 + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=17, wide=5, tall=3, brow=7, bcol=2, lrow=1,
               lcol=2, lspacing=1, lcolors=[2, 3, 7], lcorners=[-1, 2, 3],
               colors=[3, 3, 7, -1, 2, 2, -1, -1, -1, -1, 2, 2, 3, 3, 7]),
      generate(width=20, height=18, wide=4, tall=3, brow=7, bcol=4, lrow=0,
               lcol=0, lspacing=2, lcolors=[2, 3, 4, 8], lcorners=[3, 2, -1, 1],
               colors=[2, -1, -1, 4, 3, 2, 3, -1, 3, -1, -1, 8]),
  ]
  test = [
      generate(width=18, height=20, wide=4, tall=4, brow=7, bcol=1, lrow=1,
               lcol=1, lspacing=1, lcolors=[3, 2, 8, 4], lcorners=[2, 3, -1, 0],
               colors=[2, 2, 2, 8, -1, 3, 3, -1, 4, 3, -1, -1, 4, -1, -1, 8]),
  ]
  return {"train": train, "test": test}
