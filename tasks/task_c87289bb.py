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


def generate(width=None, height=None, bcols=None, cols=None, wides=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    bcols: The columns of the blue lines.
    cols: The columns of the red lines.
    wides: The widths of the red lines.
  """

  def draw():
    grid, output = common.grids(width, height)
    brow = 2 if height < 10 else 3  # where the blue lines end
    rrow = brow + 2 if width <= 12 else brow + 1  # where the red lines live
    for col, wide in zip(cols, wides):
      for c in range(wide):
        output[rrow][col + c] = grid[rrow][col + c] = 2
    for bcol in bcols:
      r, col = 0, bcol
      while r < height:
        if col == bcol and r <= brow: grid[r][col] = 8
        if output[r][col] == 8: return None, None  # overlaps with another line.
        output[r][col] = 8
        if common.get_pixel(grid, r + 1, col) != 2:
          r += 1
        else:
          cdir, dist = 0, 1
          while cdir == 0:  # Figure out whether to go left or right.
            if common.get_pixel(grid, r + 1, col - dist) != 2: cdir = -1
            if common.get_pixel(grid, r + 1, col + dist) != 2: cdir = +1
            dist += 1
          col += cdir
    return grid, output

  if width is None:
    height, width = common.randint(9, 10), common.randint(9, 15)
    while True:
      bcol, bcols = common.randint(0, 1), []
      while bcol < width:
        bcols.append(bcol)
        bcol += common.randint(2, 4)
      col, cols = common.randint(1, 5), []
      wide, wides = common.randint(2, 3), []
      while col + wide + 1 < width:
        cols.append(col)
        wides.append(wide)
        col += wide + common.randint(1, 4)
        wide = common.randint(2, 4)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=10, bcols=[1, 5, 7, 10], cols=[1, 5], wides=[2, 3]),
      generate(width=12, height=10, bcols=[1, 3, 5, 7, 9, 11], cols=[5], wides=[3]),
      generate(width=12, height=10, bcols=[0, 2, 6, 9, 11], cols=[2, 5], wides=[2, 3]),
      generate(width=10, height=9, bcols=[1, 5, 9], cols=[4], wides=[3]),
  ]
  test = [
      generate(width=15, height=10, bcols=[1, 4, 7, 10, 13], cols=[4, 10], wides=[2, 4]),
  ]
  return {"train": train, "test": test}
