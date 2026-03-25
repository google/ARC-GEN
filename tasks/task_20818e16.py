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


def generate(width=None, height=None, wides=None, talls=None, rows=None,
             cols=None, colors=None, bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid.
    height: the height of the grid.
    wides: the widths of the boxes.
    talls: the heights of the boxes.
    rows: the rows of the boxes.
    cols: the columns of the boxes.
    colors: the colors of the boxes.
    bgcolor: the background color of the grid.
  """

  def draw():
    grid = common.grid(width, height, bgcolor)
    output = common.grid(max(wides), max(talls))
    for wide, tall, row, col, color in zip(wides, talls, rows, cols, colors):
      common.rect(grid, wide, tall, row, col, color)
    area_and_index = [(w * t, i) for i, (w, t) in enumerate(zip(wides, talls))]
    area_and_index = sorted(area_and_index, reverse=True)
    for _, index in area_and_index:
      common.rect(output, wides[index], talls[index], 0, 0, colors[index])
    return grid, output

  if width is None:
    width, height = common.randint(14, 16), common.randint(14, 16)
    num_boxes = common.randint(3, 4)
    while True:
      # First, create monotonically increasing wides and talls.
      wides = sorted(common.choices(list(range(1, 11)), num_boxes))
      talls = sorted(common.choices(list(range(1, 11)), num_boxes))
      good = True
      for i in range(1, num_boxes):
        if wides[i] == wides[i - 1] and talls[i] == talls[i - 1]: good = False
      if not good: continue
      # Second, shuffle them up!
      order = common.shuffle(list(range(num_boxes)))
      wides = [wides[i] for i in order]
      talls = [talls[i] for i in order]
      # Third, find rows and cols (overlap OK).
      rows = [common.randint(0, height - tall) for tall in talls]
      cols = [common.randint(0, width - wide) for wide in wides]
      bgcolor = common.randint(0, 9)
      colors = list(range(1, 10))
      if bgcolor in colors: colors.remove(bgcolor)
      colors = common.sample(colors, num_boxes)
      if not common.overlaps(rows, cols, wides, talls): break
      # Fourth, make sure some corners of each box are visible.
      grid, _ = draw()
      for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
        if grid[row][col] == color and grid[row + tall - 1][col + wide - 1] == color:
          continue
        if grid[row + tall - 1][col] == color and grid[row][col + wide - 1] == color:
          continue
        good = False
      if good: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=16, wides=[6, 9, 2], talls=[6, 6, 2],
               rows=[5, 0, 11], cols=[2, 5, 10], colors=[3, 2, 5], bgcolor=8),
      generate(width=15, height=14, wides=[8, 5, 4], talls=[6, 5, 2],
               rows=[1, 4, 9], cols=[2, 6, 1], colors=[2, 1, 3], bgcolor=4),
      generate(width=15, height=15, wides=[5, 8, 4, 2], talls=[5, 8, 3, 1],
               rows=[1, 3, 9, 1], cols=[1, 4, 2, 11], colors=[4, 6, 3, 8],
               bgcolor=0),
  ]
  test = [
      generate(width=16, height=16, wides=[10, 4, 3, 2], talls=[6, 4, 2, 1],
               rows=[1, 5, 10, 13], cols=[2, 6, 8, 3], colors=[2, 3, 8, 6],
               bgcolor=1),
  ]
  return {"train": train, "test": test}
