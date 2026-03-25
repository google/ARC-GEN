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


def generate(bgcolor=None, colors=None, wides=None, talls=None, brows=None,
             bcols=None, bcolors=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    bgcolor: The background color.
    colors: The colors to use for the input grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row indices of the boxes.
    bcols: The column indices of the boxes.
    bcolors: The colors of the boxes.
    prows: The row indices of the pixels.
    pcols: The column indices of the pixels.
  """

  if bgcolor is None:
    subset = common.random_colors(common.randint(5, 6))
    bgcolor = subset.pop()
    colors = common.sample(subset, 3)
    num_boxes = common.randint(5, 8)
    while True:
      sides = [common.randint(0, 2) for _ in range(num_boxes)]
      wides, talls = [], []
      for side in sides:
        if side == 0:
          wide, tall = 1, common.randint(2, 4)
        elif side == 1:
          wide, tall = common.randint(2, 4), 1
        else:
          wide, tall = 2, 2
        wides.append(wide)
        talls.append(tall)
      brows = [common.randint(1, 12 - tall) for tall in talls]
      bcols = [common.randint(1, 9 - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1):
        break
    bcolors = common.choices(subset, num_boxes)
    prows, pcols = [], []
    idx = common.randint(0, num_boxes - 1)
    if wides[idx] == 2 and talls[idx] == 2:
      prows.append(brows[idx] + common.randint(0, 1))
      pcols.append(bcols[idx] + common.randint(0, 1))

  grid, output = common.grids(10, 20)
  for i, color in enumerate(colors):
    grid[2 * i + 1][0] = color
    for c in range(bcolors.count(color)):
      output[2 * i + 1][c] = color
  common.rect(grid, 10, 13, 7, 0, bgcolor)
  common.rect(output, 10, 13, 7, 0, bgcolor)
  for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
    common.rect(grid, wide, tall, 7 + brow, bcol, bcolor)
    if bcolor in colors: common.rect(output, wide, tall, 7 + brow, bcol, bcolor)
  for prow, pcol in zip(prows, pcols):
    output[7 + prow][pcol] = grid[7 + prow][pcol] = bgcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(bgcolor=3, colors=[2, 8, 4], wides=[2, 1, 1, 2, 2, 3, 2, 2],
               talls=[2, 3, 4, 1, 2, 1, 2, 1],
               brows=[1, 1, 1, 4, 6, 7, 9, 10],
               bcols=[1, 6, 8, 2, 2, 5, 1, 7],
               bcolors=[1, 2, 8, 2, 8, 4, 2, 2], prows=[], pcols=[]),
      generate(bgcolor=1, colors=[4, 2, 3], wides=[2, 2, 1, 1, 2, 4],
               talls=[2, 2, 2, 3, 2, 1], brows=[1, 2, 2, 6, 6, 10],
               bcols=[1, 5, 8, 2, 5, 3], bcolors=[2, 2, 3, 8, 3, 3],
               prows=[2], pcols=[2]),
      generate(bgcolor=8, colors=[1, 2, 4],
               wides=[2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 4],
               talls=[1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1],
               brows=[1, 1, 2, 3, 3, 6, 6, 6, 8, 9, 11],
               bcols=[1, 8, 6, 1, 3, 1, 3, 7, 5, 2, 5],
               bcolors=[2, 4, 1, 6, 4, 4, 2, 3, 6, 1, 4], prows=[], pcols=[]),
  ]
  test = [
      generate(bgcolor=4, colors=[2, 8, 3], wides=[3, 2, 2, 2, 2, 1, 2, 2, 2],
               talls=[1, 1, 1, 2, 2, 3, 2, 2, 1],
               brows=[1, 1, 3, 3, 5, 6, 7, 10, 11],
               bcols=[1, 6, 1, 6, 1, 8, 4, 1, 6],
               bcolors=[2, 3, 7, 2, 3, 2, 5, 2, 2], prows=[], pcols=[]),
  ]
  return {"train": train, "test": test}
