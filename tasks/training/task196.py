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


def generate(size=None, rows=None, cols=None, wides=None, talls=None,
             grows=None, gcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    grows: a list of vertical coordinates where gaps should be placed
    gcols: a list of horizontal coordinates where gaps should be placed
  """
  if size is None:
    size = 3 * common.randint(3, 5)
    num_boxes = common.randint(size // 4, size // 2)
    while True:
      wides = [common.randint(1, 5) for _ in range(num_boxes)]
      talls = [common.randint(1, 5) for _ in range(num_boxes)]
      rows = [common.randint(0, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      if common.overlaps(rows, cols, wides, talls, 1): continue
      grows, gcols, some_closed = [], [], False
      for wide, tall in zip(wides, talls):
        if wide == 1 or tall == 1:  # Never take a chunk of flat shapes.
          grows.append(-1)
          gcols.append(-1)
        elif wide != 2 and tall != 2 and common.randint(0, 1):
          grows.append(-1)
          gcols.append(-1)
          some_closed = True
        elif min(wide, tall) >= 3:  # Don't take a corner if shape has a hole.
          if common.randint(0, 1):
            grows.append(0 if common.randint(0, 1) else (tall - 1))
            gcols.append(common.randint(1, wide - 2))
          else:
            grows.append(common.randint(1, tall - 2))
            gcols.append(0 if common.randint(0, 1) else (wide - 1))
        else:  # Take chunks from any 2xH or Wx2 boxes, and half of all others.
          grows.append(0 if common.randint(0, 1) else (tall - 1))
          gcols.append(0 if common.randint(0, 1) else (wide - 1))
      if some_closed: break

  grid, output = common.grids(size, size)
  for row, col, w, t, grow, gcol in zip(rows, cols, wides, talls, grows, gcols):
    for r in range(row, row + t):
      common.draw(grid, r, col, common.blue())
      common.draw(grid, r, col + w - 1, common.blue())
      color = common.green()
      if w < 3 or t < 3 or grow > -1 or gcol > -1: color = common.blue()
      common.draw(output, r, col, color)
      common.draw(output, r, col + w - 1, color)
    for c in range(col, col + w):
      common.draw(grid, row, c, common.blue())
      common.draw(grid, row + t - 1, c, common.blue())
      color = common.green()
      if w < 3 or t < 3 or grow > -1 or gcol > -1: color = common.blue()
      common.draw(output, row, c, color)
      common.draw(output, row + t - 1, c, color)
    if grow > -1 and gcol > -1:
      grid[row + grow][col + gcol] = common.black()
      output[row + grow][col + gcol] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, rows=[1, 2, 6, 7, 7, 10, 12, 13],
               cols=[10, 2, 12, 3, 6, 0, 10, 5],
               wides=[3, 4, 2, 1, 4, 3, 4, 2],
               talls=[3, 3, 2, 1, 4, 4, 3, 1],
               grows=[2, -1, 1, -1, -1, -1, -1, -1],
               gcols=[1, -1, 1, -1, -1, -1, -1, -1]),
      generate(size=15, rows=[3, 3, 8, 8],
               cols=[4, 10, 4, 9],
               wides=[3, 1, 1, 4],
               talls=[3, 2, 1, 3],
               grows=[-1, -1, -1, 0],
               gcols=[-1, -1, -1, 1]),
      generate(size=9, rows=[2, 6, 7], cols=[1, -1, 4],
               wides=[5, 3, 2],
               talls=[3, 3, 1],
               grows=[-1, 2, -1],
               gcols=[-1, 1, -1]),
  ]
  test = [
      generate(size=12, rows=[0, 1, 6, 7, 8, 8],
               cols=[7, 1, 1, 4, 1, 11],
               wides=[5, 4, 2, 5, 1, 1],
               talls=[5, 3, 1, 4, 1, 1],
               grows=[4, -1, -1, -1, -1, -1],
               gcols=[2, -1, -1, -1, -1, -1]),
  ]
  return {"train": train, "test": test}
