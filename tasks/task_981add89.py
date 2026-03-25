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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             bcolors=None, pcols=None, pcolors=None, bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  def draw():
    same_color, diff_color = False, False
    grid, output = common.grids(size, size, bgcolor)
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      # Try to avoid boxes overlapping others with the same color.
      for r in range(brow, brow + tall):
        for c in range(bcol, bcol + wide):
          if grid[r][c] == bcolor: return None, None
      common.rect(grid, wide, tall, brow, bcol, bcolor)
      common.rect(output, wide, tall, brow, bcol, bcolor)
    for pcol, pcolor in zip(pcols, pcolors):
      grid[0][pcol] = pcolor
      for r in range(size):
        if output[r][pcol] == pcolor: same_color = True
        elif output[r][pcol] != bgcolor: diff_color = True
        output[r][pcol] = bgcolor if output[r][pcol] == pcolor else pcolor
    if not same_color or not diff_color: return None, None
    return grid, output

  if size is None:
    size = 20 if common.randint(0, 1) else 30
    num_boxes = common.randint(1, 3) if size == 20 else common.randint(4, 6)
    bgcolor = common.random_color()
    while True:
      wides = [common.randint(5, size - 10) for _ in range(num_boxes)]
      talls = [common.randint(5, size - 10) for _ in range(num_boxes)]
      brows = [common.randint(1, size - tall - 1) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      bcolors = [common.random_color(exclude=[bgcolor]) for _ in range(num_boxes)]
      pcol, pcols = common.randint(2, 5), []
      while pcol < size - 1:
        pcols.append(pcol)
        pcol += common.randint(3, 7)
      pcolors = [common.random_color(exclude=[bgcolor]) for _ in range(len(pcols))]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, wides=[9], talls=[6], brows=[6], bcols=[2], bcolors=[2],
               pcols=[5, 9], pcolors=[2, 4], bgcolor=8),
      generate(size=30, wides=[11, 11, 12, 6, 12, 8],
               talls=[10, 11, 9, 10, 9, 8], brows=[13, 3, 1, 7, 19, 19],
               bcols=[6, 15, 1, 24, 1, 19], bcolors=[2, 3, 1, 9, 8, 4],
               pcols=[2, 5, 9, 20, 28], pcolors=[8, 3, 2, 4, 8], bgcolor=7),
  ]
  test = [
      generate(size=30, wides=[14, 14, 6, 13, 19, 8], talls=[14, 5, 6, 8, 6, 6],
               brows=[2, 3, 10, 13, 20, 23], bcols=[0, 16, 21, 4, 11, 1],
               bcolors=[1, 3, 9, 2, 8, 1], pcols=[3, 7, 12, 18, 23, 27],
               pcolors=[1, 2, 3, 3, 9, 8], bgcolor=4),
  ]
  return {"train": train, "test": test}
