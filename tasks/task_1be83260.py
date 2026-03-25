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
             bcol=None, prow=None, pcol=None, bgcolor=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The number of pixels vertically.
    tall: The number of pixels horizontally.
    brow: The row of the boxes in the input.
    bcol: The column of the boxes in the input.
    prow: The row of the box to show the colors.
    pcol: The column of the box to show the colors.
    bgcolor: The background color of the boxes.
    colors: The colors of the pixels.
  """

  if width is None:
    wide, tall = common.randint(2, 3), common.randint(2, 3)
    outwidth = wide * (2 * (wide + 1)) - 1
    outheight = tall * (2 * (tall + 1)) - 1
    width = common.randint(outwidth + 2, 30)
    height = common.randint(outheight + 2, 30)
    brow = common.randint(1, height - outheight - 1)
    bcol = common.randint(1, width - outwidth - 1)
    prow = common.randint(0, tall - 1)
    pcol = common.randint(0, wide - 1)
    bgcolor = common.random_color()
    while True:
      colors = [common.random_color(exclude=[bgcolor]) for _ in range(wide * tall)]
      colors = [color if common.randint(0, 1) else -1 for color in colors]
      if -1 in colors and len(set(colors)) >= 4: break

  outwidth = wide * (2 * (wide + 1)) - 1
  outheight = tall * (2 * (tall + 1)) - 1
  grid = common.grid(width, height)
  output = common.grid(outwidth, outheight, bgcolor)
  w, t = 2 * wide + 1, 2 * tall + 1
  for row in range(tall):
    for col in range(wide):
      common.rect(grid, w, t, brow + row * (t + 1), bcol + col * (w + 1), bgcolor)
      color = colors[row * wide + col]
      if color != -1:
        common.rect(output, w, t, row * (t + 1), col * (w + 1), color)
      for r in range(tall):
        for c in range(wide):
          color = colors[r * wide + c]
          if color != -1:
            the_color = 0 if row != prow or col != pcol else color
            grid[brow + row * (t + 1) + 2 * r + 1][bcol + col * (w + 1) + 2 * c + 1] = the_color
            output[row * (t + 1) + 2 * r + 1][col * (w + 1) + 2 * c + 1] = bgcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=27, wide=2, tall=3, brow=1, bcol=1, prow=2,
               pcol=0, bgcolor=2, colors=[3, 1, 4, -1, 3, 1]),
      generate(width=19, height=17, wide=2, tall=2, brow=2, bcol=2, prow=1,
               pcol=1, bgcolor=1, colors=[2, 8, 4, -1]),
  ]
  test = [
      generate(width=25, height=16, wide=3, tall=2, brow=1, bcol=1, prow=0,
               pcol=2, bgcolor=8, colors=[4, -1, 3, 2, 3, -1]),
      generate(width=27, height=27, wide=3, tall=3, brow=1, bcol=2, prow=1,
               pcol=1, bgcolor=3, colors=[4, 4, -1, -1, -1, 2, -1, 8, 7]),
  ]
  return {"train": train, "test": test}
