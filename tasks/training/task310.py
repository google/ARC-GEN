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


def generate(size=None, spacings=None, colors=None, boxcolor=None,
             boxlength=None, boxrow=None, boxcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    spacings: a list of spacings between wires on the grid
    colors: a list of colors for wires on the grid
    boxcolor: the color of the box
    boxlength: the length of the box
    boxrow: the row of the box
    boxcol: the column of the box
  """
  if size is None:
    size, num_wires = common.randint(20, 30), common.randint(3, 4)
    spacings = common.sample([3, 4, 5, 6], num_wires)
    colors = common.random_colors(num_wires + 1)
    boxcolor, boxlength = colors.pop(), common.randint(5, 8)
    boxrow = common.randint(0, size - boxlength)
    boxcol = common.randint(0, size - boxlength)

  grid = common.grid(size, size)
  output = common.grid(boxlength, boxlength)
  for color, spacing in zip(colors, spacings):
    for r in range(size):
      for c in range(size):
        if (r + 1) % spacing != 0 and (c + 1) % spacing != 0: continue
        grid[r][c] = color
        if r < boxrow or r >= boxrow + boxlength: continue
        if c < boxcol or c >= boxcol + boxlength: continue
        output[r - boxrow][c - boxcol] = color
  for i in range(boxlength):
    for dr, dc in [(0, i), (boxlength - 1, i), (i, 0), (i, boxlength - 1)]:
      output[dr][dc] = grid[boxrow + dr][boxcol + dc] = boxcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=24, spacings=[5, 3, 4, 6], colors=[8, 2, 4, 5], boxcolor=3,
               boxlength=7, boxrow=5, boxcol=5),
      generate(size=26, spacings=[5, 4, 3], colors=[1, 3, 8], boxcolor=2,
               boxlength=7, boxrow=2, boxcol=2),
      generate(size=28, spacings=[4, 5, 3, 6], colors=[1, 8, 3, 5], boxcolor=6,
               boxlength=7, boxrow=17, boxcol=5),
  ]
  test = [
      generate(size=24, spacings=[3, 4, 5, 6], colors=[1, 2, 3, 4], boxcolor=8,
               boxlength=6, boxrow=14, boxcol=14),
  ]
  return {"train": train, "test": test}
