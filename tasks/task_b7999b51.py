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
             bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid.
    height: the height of the grid.
    wides: the widths of the boxes.
    talls: the heights of the boxes.
    brows: the rows of the boxes.
    bcols: the columns of the boxes.
    colors: the colors of the boxes.
  """

  def draw():
    grid = common.grid(width, height)
    output = common.grid(len(talls), max(talls))
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      common.rect(grid, wide, tall, brow, bcol, color)
    for i, (tall, color) in enumerate(sorted(zip(talls, colors), reverse=True)):
      common.rect(output, 1, tall, 0, i, color)
    # Now check that some pair of diagonal corners is visible for each box.
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      if grid[brow][bcol] == color and grid[brow + tall - 1][bcol + wide - 1] == color:
        continue
      if grid[brow][bcol + wide - 1] == color and grid[brow + tall - 1][bcol] == color:
        continue
      return None, None
    return grid, output

  if width is None:
    width, height = common.randint(15, 18), common.randint(10, 20)
    boxes = common.randint(2, 5)
    colors = common.random_colors(boxes)
    while True:
      talls = common.sample(range(1, 6), boxes)
      wides = [common.randint(4, 12 - tall) for tall in talls]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls): continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=10, wides=[7, 5, 6], talls=[3, 2, 1],
               brows=[1, 5, 3], bcols=[2, 3, 5], colors=[2, 1, 3]),
      generate(width=18, height=19, wides=[5, 7, 12, 8], talls=[3, 5, 1, 4],
               brows=[2, 6, 3, 8], bcols=[2, 4, 3, 6], colors=[1, 8, 2, 7]),
      generate(width=15, height=10, wides=[4, 6, 4], talls=[3, 4, 1],
               brows=[1, 5, 6], bcols=[1, 2, 1], colors=[8, 4, 3]),
  ]
  test = [
      generate(width=18, height=12, wides=[6, 6, 6, 4, 5],
               talls=[3, 5, 6, 2, 1], brows=[2, 3, 6, 2, 6],
               bcols=[1, 4, 1, 9, 7], colors=[2, 3, 6, 1, 8]),
  ]
  return {"train": train, "test": test}
