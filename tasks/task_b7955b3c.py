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


def generate(width=None, height=None, bgcolor=None, wides=None, talls=None,
             brows=None, bcols=None, bcolors=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    bgcolor: The background color of the grids.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row indices of the tops of the boxes.
    bcols: The column indices of the left sides of the boxes.
    bcolors: The colors of the boxes.
    prows: The row indices of the plusses.
    pcols: The column indices of the plusses.
  """

  def draw():
    # Make sure the plusses are spaced apart from each other.
    if common.overlaps(prows, pcols, [4] * len(prows), [4] * len(pcols)):
      return None, None
    grid, output = common.grids(width, height, bgcolor)
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      common.rect(grid, wide, tall, brow, bcol, bcolor)
      common.rect(output, wide, tall, brow, bcol, bcolor)
    for prow, pcol in zip(prows, pcols):
      for dr, dc in [(0, -1), (0, 1), (1, 0), (-1, 0), (0, 0)]:
        grid[prow + dr][pcol + dc] = 8
    # Make sure that at least three corners per box are visible.
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      num_corners = 0
      if grid[brow][bcol] == bcolor: num_corners += 1
      if grid[brow + tall - 1][bcol] == bcolor: num_corners += 1
      if grid[brow][bcol + wide - 1] == bcolor: num_corners += 1
      if grid[brow + tall - 1][bcol + wide - 1] == bcolor: num_corners += 1
      if num_corners < 3: return None, None
    # If two boxes overlap, make sure we can distinguish the order in the input.
    for j in range(len(wides)):
      for i in range(j):
        min_row = max(brows[i], brows[j])
        max_row = min(brows[i] + talls[i], brows[j] + talls[j])
        min_col = max(bcols[i], bcols[j])
        max_col = min(bcols[i] + wides[i], bcols[j] + wides[j])
        if min_row >= max_row or min_col >= max_col: continue
        seen = False
        for row in range(min_row, max_row):
          for col in range(min_col, max_col):
            if grid[row][col] == bcolors[j]: seen = True
        if not seen: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(8, 27), common.randint(8, 27)
    num_boxes = 2
    if width * height >= 125: num_boxes = 3
    if width * height >= 250: num_boxes = 4
    if width * height >= 375: num_boxes = 5
    if width * height >= 500: num_boxes = 6
    num_plusses = common.randint(num_boxes // 2, num_boxes)
    bcolors = common.sample([0, 1, 2, 3, 4, 5, 6, 7, 9], num_boxes + 1)
    bgcolor = bcolors.pop()
    while True:
      wides = [common.randint(1, width - 2) for _ in range(num_boxes)]
      talls = [common.randint(1, height - 2) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      prows = [common.randint(1, height - 2) for _ in range(num_plusses)]
      pcols = [common.randint(1, width - 2) for _ in range(num_plusses)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=18, bgcolor=9, wides=[9, 9, 4, 9, 8],
               talls=[14, 5, 4, 2, 4], brows=[1, 5, 3, 2, 12],
               bcols=[1, 4, 2, 4, 4], bcolors=[0, 1, 4, 7, 6],
               prows=[4, 4, 10, 15, 16], pcols=[4, 11, 5, 9, 2]),
      generate(width=14, height=10, bgcolor=5, wides=[8, 2, 6, 8],
               talls=[7, 8, 1, 3], brows=[0, 1, 2, 5], bcols=[1, 11, 6, 4],
               bcolors=[6, 7, 4, 3], prows=[4, 7], pcols=[8, 4]),
      generate(width=8, height=10, bgcolor=4, wides=[3, 2], talls=[6, 7],
               brows=[1, 2], bcols=[1, 5], bcolors=[3, 2], prows=[4],
               pcols=[5]),
  ]
  test = [
      generate(width=22, height=26, bgcolor=1, wides=[19, 5, 17, 6, 12, 3],
               talls=[4, 20, 5, 20, 6, 13], brows=[1, 2, 9, 2, 19, 10],
               bcols=[2, 15, 2, 4, 6, 11], bcolors=[2, 3, 4, 6, 7, 9],
               prows=[1, 6, 9, 13, 18, 21], pcols=[16, 6, 18, 10, 14, 6]),
      generate(width=22, height=18, bgcolor=3, wides=[4, 4, 4, 18, 18],
               talls=[16, 16, 16, 5, 4], brows=[1, 1, 1, 3, 11],
               bcols=[2, 8, 14, 3, 3], bcolors=[2, 1, 0, 7, 9],
               prows=[2, 3, 7, 11, 14, 14], pcols=[13, 5, 8, 10, 4, 17]),
  ]
  return {"train": train, "test": test}
