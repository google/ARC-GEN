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


def generate(inwidth=None, inheight=None, outwidth=None, outheight=None,
             brow=None, bcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    inwidth: The width of the input grid.
    inheight: The height of the input grid.
    outwidth: The width of the output grid.
    outheight: The height of the output grid.
    brow: The row of the subgrid.
    bcol: The column of the subgrid.
    colors: The colors of the input grid.
  """

  if inwidth is None:
    inwidth = 20 + common.randint(0, 6) - 3
    inheight = 20 + common.randint(0, 6) - 3
    area = inwidth * inheight
    colors = common.random_colors(3)
    fgcolor, bgcolor, linecolor = colors[0], colors[1], colors[2]
    colors = [bgcolor if common.randint(0, 4) else fgcolor for _ in range(area)]
    # Draw the lines.
    mini = common.randint(4, 5)
    for r in range(mini - 1, inheight, mini):
      for c in range(inwidth):
        colors[r * inwidth + c] = linecolor
    for c in range(mini - 1, inwidth, mini):
      for r in range(inheight):
        colors[r * inwidth + c] = linecolor
    # Choose the subgrid to select.
    upper = 3 if mini == 4 else 2
    wide, tall = common.randint(1, upper), common.randint(1, upper)
    brow = mini * common.randint(0, upper - tall) + mini - 1
    bcol = mini * common.randint(0, upper - wide) + mini - 1
    outwidth, outheight = mini * wide + 1, mini * tall + 1
    # Mark the corners.
    colors[brow * inwidth + bcol] = bgcolor
    colors[brow * inwidth + bcol + outwidth - 1] = bgcolor
    colors[(brow + outheight - 1) * inwidth + bcol] = bgcolor
    colors[(brow + outheight - 1) * inwidth + bcol + outwidth - 1] = bgcolor

  grid = common.grid(inwidth, inheight)
  output = common.grid(outwidth, outheight)
  for i, color in enumerate(colors):
    grid[i // inwidth][i % inwidth] = color
  for r in range(outheight):
    for c in range(outwidth):
      output[r][c] = grid[brow + r][bcol + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(inwidth=21, inheight=17, outwidth=9, outheight=9, brow=3, bcol=3,
               colors=[3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3,
                       3, 3, 3, 1, 2, 3, 3, 1, 3, 3, 3, 1, 3, 3, 2, 1, 3, 3, 3, 1, 3,
                       3, 3, 3, 1, 3, 3, 2, 1, 3, 3, 3, 1, 3, 3, 3, 1, 2, 3, 2, 1, 2,
                       1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3,
                       3, 2, 3, 1, 3, 2, 3, 1, 3, 3, 3, 1, 2, 3, 3, 1, 3, 3, 3, 1, 3,
                       2, 3, 3, 1, 3, 3, 3, 1, 3, 3, 2, 1, 3, 2, 3, 1, 3, 3, 3, 1, 3,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3,
                       3, 3, 2, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 2, 1, 3,
                       3, 3, 3, 1, 3, 3, 3, 1, 2, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3,
                       1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 2, 3, 1, 3,
                       3, 3, 3, 1, 3, 3, 2, 1, 2, 3, 2, 1, 3, 2, 3, 1, 3, 3, 3, 1, 3,
                       3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 2, 3, 1, 3, 3, 3, 1, 2,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       3, 3, 3, 1, 3, 3, 2, 1, 3, 2, 2, 1, 2, 3, 3, 1, 3, 3, 3, 1, 3]),
      generate(inwidth=22, inheight=18, outwidth=11, outheight=6, brow=4, bcol=4,
               colors=[8, 1, 8, 8, 2, 8, 8, 1, 8, 2, 8, 8, 8, 1, 2, 8, 8, 8, 8, 2, 8, 1,
                       8, 8, 8, 8, 2, 8, 8, 1, 8, 2, 8, 8, 8, 1, 2, 8, 8, 8, 8, 2, 1, 8,
                       8, 1, 1, 8, 2, 8, 1, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8,
                       8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8,
                       2, 2, 2, 2, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 2, 2, 2, 2, 2, 2, 2,
                       8, 8, 8, 8, 2, 8, 8, 1, 1, 2, 8, 8, 8, 8, 2, 1, 8, 8, 8, 2, 8, 8,
                       1, 1, 8, 1, 2, 8, 8, 8, 1, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8,
                       8, 8, 1, 8, 2, 8, 8, 8, 8, 2, 8, 8, 1, 8, 2, 8, 8, 1, 8, 2, 8, 8,
                       8, 8, 8, 8, 2, 8, 1, 8, 1, 2, 8, 8, 8, 8, 2, 8, 1, 8, 8, 2, 8, 8,
                       2, 2, 2, 2, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 2, 2, 2, 2, 2, 2, 2,
                       1, 1, 8, 8, 2, 8, 8, 8, 8, 2, 1, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8,
                       8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8,
                       8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 1, 8, 8, 2, 1, 8,
                       8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 1,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 1, 2, 1, 8, 8, 1, 2, 1, 8,
                       1, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8,
                       1, 8, 1, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8, 8, 8, 2, 8, 8]),
  ]
  test = [
      generate(inwidth=20, inheight=19, outwidth=6, outheight=11, brow=4, bcol=4,
               colors=[4, 4, 4, 7, 2, 4, 4, 4, 4, 2, 7, 4, 4, 4, 2, 4, 4, 4, 4, 2,
                       4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 7, 4, 7, 4, 2, 4, 4, 4, 4, 2,
                       4, 4, 4, 4, 2, 4, 4, 7, 4, 2, 4, 4, 7, 4, 2, 4, 4, 7, 4, 2,
                       4, 4, 4, 7, 2, 4, 4, 4, 4, 2, 7, 4, 7, 4, 2, 7, 4, 4, 7, 2,
                       2, 2, 2, 2, 4, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       4, 7, 4, 4, 2, 4, 4, 4, 4, 2, 4, 4, 4, 7, 2, 4, 4, 4, 4, 2,
                       4, 4, 4, 4, 2, 7, 7, 4, 4, 2, 4, 4, 4, 4, 2, 4, 7, 4, 7, 2,
                       4, 4, 7, 4, 2, 4, 7, 4, 4, 2, 4, 7, 4, 4, 2, 7, 4, 4, 4, 2,
                       4, 4, 7, 4, 2, 4, 4, 4, 7, 2, 4, 4, 4, 4, 2, 4, 7, 4, 4, 2,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       4, 4, 4, 4, 2, 7, 4, 4, 4, 2, 4, 7, 4, 4, 2, 7, 4, 7, 7, 2,
                       4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 4, 7, 4, 4, 2,
                       4, 4, 7, 4, 2, 4, 4, 4, 4, 2, 4, 4, 4, 7, 2, 4, 4, 7, 4, 2,
                       4, 4, 7, 4, 2, 4, 4, 4, 4, 2, 4, 7, 7, 4, 2, 4, 7, 4, 4, 2,
                       2, 2, 2, 2, 4, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                       4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 7, 4, 4, 4, 2, 4, 4, 4, 7, 2,
                       4, 4, 4, 4, 2, 4, 4, 4, 4, 2, 7, 4, 4, 4, 2, 7, 4, 4, 7, 2,
                       4, 4, 4, 7, 2, 7, 4, 7, 4, 2, 7, 4, 4, 4, 2, 4, 4, 4, 7, 2,
                       4, 4, 4, 4, 2, 7, 4, 4, 4, 2, 4, 4, 7, 4, 2, 4, 7, 4, 4, 2]),
  ]
  return {"train": train, "test": test}
