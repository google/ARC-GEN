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


def generate(width=None, height=None, rows=None, cols=None, groups=None,
             grows=None, gcols=None, gcolors=None, trow=None, tcol=None,
             tcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: Width of the input grid.
    height: Height of the input grid.
    rows: Rows of each pixel in each group.
    cols: Columns of each pixel in each group.
    groups: Which group each pixel belongs to.
    grows: Row locations of the groups.
    gcols: Column locations of the groups.
    gcolors: Colors of each group.
    trow: Row location of the T.
    tcol: Column location of the T.
    tcolor: Color of the T.
  """

  if width is None:
    width, height = common.randint(12, 16), common.randint(12, 16)
    trow, tcol = common.randint(3, height - 3), common.randint(3, width - 3)
    gcolors = common.random_colors(5)
    tcolor = gcolors.pop()
    rows, cols, groups, grows, gcols = [], [], [], [], []
    for group in range(4):
      while True:
        the_rows, the_cols = common.conway_sprite(3, 3)
        if common.diagonally_connected(list(zip(the_rows, the_cols))): break
      rows.extend(the_rows)
      cols.extend(the_cols)
      groups.extend([group] * len(the_rows))
      grow, gcol = common.randint(0, trow - 3), common.randint(0, tcol - 3)
      if group in [2, 3]:
        grow = common.randint(trow + 1, height - 3)
      if group in [1, 3]:
        gcol = common.randint(tcol + 1, width - 3)
      grows.append(grow)
      gcols.append(gcol)

  grid, output = common.grid(width, height), common.grid(6, 6)
  for row, col, group in zip(rows, cols, groups):
    grow, gcol, gcolor = grows[group], gcols[group], gcolors[group]
    row_offset = 0 if group in [0, 1] else 3
    col_offset = 0 if group in [0, 2] else 3
    grid[grow + row][gcol + col] = gcolor
    output[row_offset + row][col_offset + col] = gcolor
  for row in range(height):
    grid[row][tcol] = tcolor
  for col in range(width):
    grid[trow][col] = tcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=15,
               rows=[0, 0, 1, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 1, 2, 0, 0, 1, 2],
               cols=[1, 2, 0, 1, 2, 1, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 2, 1, 0],
               groups=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3],
               grows=[5, 2, 11, 12], gcols=[0, 7, 0, 7], gcolors=[2, 3, 5, 8],
               trow=9, tcol=4, tcolor=1),
      generate(width=13, height=12,
               rows=[0, 0, 1, 2, 2, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0, 0, 1, 2],
               cols=[0, 1, 1, 1, 2, 1, 2, 0, 1, 1, 1, 0, 2, 1, 0, 1, 1, 2],
               groups=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
               grows=[0, 0, 7, 8], gcols=[2, 10, 1, 9], gcolors=[1, 3, 4, 5],
               trow=3, tcol=7, tcolor=2),
      generate(width=12, height=16,
               rows=[0, 0, 1, 1, 2, 0, 0, 1, 2, 0, 1, 1, 1, 2, 0, 1, 1, 2, 2, 2],
               cols=[1, 2, 0, 2, 1, 1, 2, 0, 1, 0, 0, 1, 2, 1, 1, 0, 2, 0, 1, 2],
               groups=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3],
               grows=[1, 0, 12, 6], gcols=[1, 8, 0, 9], gcolors=[2, 1, 4, 5],
               trow=4, tcol=6, tcolor=3),
  ]
  test = [
      generate(width=13, height=14,
               rows=[0, 0, 1, 2, 2, 0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[1, 2, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 2, 0, 1, 1, 0, 2, 1],
               groups=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3],
               grows=[3, 2, 11, 10], gcols=[1, 9, 1, 9], gcolors=[2, 3, 6, 4],
               trow=7, tcol=6, tcolor=1),
  ]
  return {"train": train, "test": test}
