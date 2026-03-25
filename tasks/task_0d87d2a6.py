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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, urows=None, ucols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    urows: The rows of the blue lines.
    ucols: The columns of the blue lines.
  """

  def draw():
    grid, output = common.grids(width, height)
    touches = False  # We expect at least one blue line to touch a box.
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      common.rect(grid, wide, tall, brow, bcol, 2)
      color = 2
      for urow in urows:
        if urow + 1 >= brow and urow <= brow + tall:
          touches = True
          color = 1
      for ucol in ucols:
        if ucol + 1 >= bcol and ucol <= bcol + wide:
          touches = True
          color = 1
      common.rect(output, wide, tall, brow, bcol, color)
    if not touches: return None, None
    for brow in urows:
      if grid[brow][0] == 2 or grid[brow][width - 1] == 2: return None, None
      grid[brow][0] = grid[brow][width - 1] = 1
      for col in range(width):
        output[brow][col] = 1
    for bcol in ucols:
      if grid[0][bcol] == 2 or grid[height - 1][bcol] == 2: return None, None
      grid[0][bcol] = grid[height - 1][bcol] = 1
      for row in range(height):
        output[row][bcol] = 1
    return grid, output

  if width is None:
    width, height = common.randint(10, 25), common.randint(10, 25)
    while True:
      boxes = common.randint(5, 10)
      wides = [common.randint(2, 9) for _ in range(boxes)]
      talls = [common.randint(2, 9) for _ in range(boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      urows = []
      urow = common.randint(2, 12)
      while urow + 1 < height:
        urows.append(urow)
        urow += common.randint(2, 12)
      ucols = []
      ucol = common.randint(2, 12)
      while ucol + 1 < width:
        ucols.append(ucol)
        ucol += common.randint(2, 12)
      if not urows and not ucols: continue  # No blue lines.
      grid, _ = draw()
      if grid is None: continue  # Rectangle covered up a blue dot.
      break  # All good!

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=10, wides=[5, 4, 3, 4, 2],
               talls=[4, 2, 3, 3, 2], brows=[2, 2, 5, 5, 7],
               bcols=[3, 14, 9, 16, 2], urows=[], ucols=[6]),
      generate(width=20, height=20, wides=[4, 5, 4, 4, 4, 5],
               talls=[3, 4, 3, 3, 3, 2], brows=[0, 2, 7, 8, 13, 16],
               bcols=[14, 6, 2, 11, 2, 14], urows=[8], ucols=[7]),
      generate(width=14, height=13, wides=[3, 3, 2, 6, 3, 5],
               talls=[4, 2, 2, 5, 5, 2], brows=[0, 2, 5, 5, 7, 11],
               bcols=[2, 7, 0, 4, 11, 1], urows=[2], ucols=[7]),
  ]
  test = [
      generate(width=25, height=23, wides=[3, 4, 3, 5, 2, 2, 5, 9, 3, 2],
               talls=[4, 4, 3, 5, 3, 3, 4, 5, 3, 2],
               brows=[0, 1, 3, 3, 6, 9, 10, 16, 16, 18],
               bcols=[9, 19, 4, 13, 22, 9, 1, 5, 21, 17],
               urows=[4, 11], ucols=[5]),
  ]
  return {"train": train, "test": test}
