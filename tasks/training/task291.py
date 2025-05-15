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


def generate(width=None, height=None, brows=None, bcols=None, wides=None,
             talls=None, colors=None, drow=None, dcol=None, dwide=None,
             dtall=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    brows: a list of vertical coordinates where boxes should be placed
    bcols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    colors: a list of digits representing a color to be used
    drow: the vertical coordinate of the donut hole
    dcol: the horizontal coordinate of the donut hole
    dwide: the width of the donut hole
    dtall: the height of the donut hole
  """
  if width is None:
    num_boxes = common.randint(4, 7)
    while True:
      width, height = common.randint(12, 18), common.randint(12, 18)
      wides = [common.randint(2, 8) for _ in range(num_boxes)]
      talls = [common.randint(2, 8) for _ in range(num_boxes)]
      if wides[0] < 3: wides[0] = 3  # Need space for the donut hole.
      if talls[0] < 3: talls[0] = 3
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls): break
    dwide = common.randint(1, wides[0] - 2)
    dtall = common.randint(1, talls[0] - 2)
    drow = common.randint(1, talls[0] - dtall - 1)
    dcol = common.randint(1, wides[0] - dwide - 1)
    colors = common.random_colors(num_boxes)

  grid, output = common.grid(width, height), common.grid(1, 1, colors[0])
  for brow, bcol, wide, tall, color in zip(brows, bcols, wides, talls, colors):
    for r in range(brow, brow + tall):
      for c in range(bcol, bcol + wide):
        grid[r][c] = color
  for r in range(brows[0] + drow, brows[0] + drow + dtall):
    for c in range(bcols[0] + dcol, bcols[0] + dcol + dwide):
      grid[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=15,
               brows=[1, 1, 3, 5, 7, 11, 11],
               bcols=[1, 8, 5, 9, 3, 0, 8],
               wides=[3, 3, 2, 3, 5, 3, 4], talls=[4, 3, 2, 3, 3, 2, 3],
               colors=[6, 3, 1, 7, 2, 4, 8], drow=1, dcol=1, dwide=1, dtall=2),
      generate(width=17, height=15,
               brows=[3, 2, 0, 6, 11],
               bcols=[7, 0, 13, 3, 10],
               wides=[4, 5, 4, 3, 5], talls=[7, 3, 6, 6, 4],
               colors=[5, 8, 7, 2, 4], drow=3, dcol=1, dwide=2, dtall=2),
      generate(width=17, height=16,
               brows=[9, 1, 2, 9],
               bcols=[2, 2, 10, 11],
               wides=[7, 6, 5, 5], talls=[5, 5, 6, 4],
               colors=[2, 1, 3, 7], drow=2, dcol=1, dwide=3, dtall=2),
  ]
  test = [
      generate(width=15, height=14,
               brows=[11, 0, 1, 6, 8, 9],
               bcols=[10, 10, 0, 9, 1, 4],
               wides=[4, 4, 8, 4, 3, 4], talls=[3, 5, 6, 4, 3, 4],
               colors=[7, 3, 2, 4, 5, 8], drow=1, dcol=1, dwide=2, dtall=1),
  ]
  return {"train": train, "test": test}
