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


def generate(height=None, left=None, right=None, bgcolor=None, leftcolor=None,
             rightcolor=None, wides=None, talls=None, brows=None, bcols=None,
             bcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: The height of the grid.
    left: The width of the left column.
    right: The width of the right column.
    bgcolor: The background color.
    leftcolor: The color of the left box.
    rightcolor: The color of the right box.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row positions of the rectangles.
    bcols: The column positions of the rectangles.
    bcolors: The colors of the rectangles.
  """

  def draw():
    if common.overlaps(brows, bcols, wides, talls, 1): return None, None
    if 1 not in brows: return None, None
    if height - 3 not in [brow + tall for brow, tall in zip(brows, talls)]:
      return None, None
    width = left + right + 3
    grid, output = common.grids(width, height, bgcolor)
    for g in [grid, output]:
      common.rect(g, left, height - 2, 1, 1, leftcolor)
      common.rect(g, right, height - 2, 1, left + 2, rightcolor)
    kinds = []
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, bcolors):
      common.rect(grid, wide, tall, brow + 1, bcol + 1, color)
      common.rect(output, wide, tall, brow + 1, bcol + 1, color)
      if wide == 2 and tall == 2:
        col = (left + 3) if bcol == 1 else (left + right - 1)
        common.rect(output, wide, tall, brow + 1, col, color)
        kinds.append(0)
      else:
        common.rect(output, right - 2, tall, brow + 1, left + 3, color)
        kinds.append(1)
    if 0 not in kinds or 1 not in kinds: return None, None
    return grid, output

  if height is None:
    height = common.randint(10, 15)
    left, right = common.randint(5, 10), common.randint(10, 15)
    colors = common.shuffle([1, 2, 3, 4, 6, 8])
    bgcolor, leftcolor, rightcolor = colors.pop(), colors.pop(), colors.pop()
    while True:
      wides, talls, brows, bcols, bcolors = [], [], [], [], []
      for _ in range(common.randint(3, 5)):
        if common.randint(0, 1):
          wides.append(2)
          talls.append(2)
          brows.append(common.randint(1, height - 5))
          bcols.append(1 if common.randint(0, 1) else (left - 3))
        else:
          wides.append(left - 2)
          talls.append(common.randint(1, 2))
          brows.append(common.randint(1, height - talls[-1] - 3))
          bcols.append(1)
        bcolors.append(common.choice(colors))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=14, left=7, right=15, bgcolor=2, leftcolor=1,
               rightcolor=4, wides=[5, 2, 2, 5], talls=[1, 2, 2, 1],
               brows=[1, 3, 7, 10], bcols=[1, 1, 4, 1], bcolors=[3, 8, 8, 3]),
      generate(height=11, left=6, right=13, bgcolor=4, leftcolor=1,
               rightcolor=2, wides=[2, 4, 2], talls=[2, 1, 2], brows=[1, 4, 6],
               bcols=[1, 1, 3], bcolors=[8, 8, 8]),
  ]
  test = [
      generate(height=12, left=8, right=15, bgcolor=3, leftcolor=1,
               rightcolor=8, wides=[2, 2, 6, 6], talls=[2, 2, 1, 2],
               brows=[1, 1, 4, 7], bcols=[1, 5, 1, 1], bcolors=[4, 2, 3, 6]),
  ]
  return {"train": train, "test": test}
