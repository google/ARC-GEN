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


def generate(rows=None, cols=None, wides=None, talls=None, colors=None,
             size=12):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of digits representing box colors (black / red)
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_boxes = min(3, common.randint(2, 5))
    # First, choose nonoverlapping positions.
    while True:
      wides = [common.randint(4, 6) for _ in range(num_boxes)]
      talls = [common.randint(4, 6) for _ in range(num_boxes)]
      rows = [common.randint(0, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break
    # Then, decide whether to manipulate the boxes, and settle on colors.
    colors = [common.black()] * num_boxes
    for i in range(num_boxes):
      wide, tall = wides[i], talls[i]
      # Sometimes we leave it alone, whether it's a square or not.
      if common.randint(0, 1):
        if wide == tall: colors[i] = common.red()
        continue
      # For squares, sometimes we'll add mini squares inside.
      if wide == tall and common.randint(0, 1):
        wides.append(wide - 1)
        talls.append(tall - 1)
        rows.append(rows[i] + common.randint(0, 1))
        cols.append(cols[i] + common.randint(0, 1))
        colors.append(common.red())
        continue
      # Finally, sometimes we add some junk -- it won't be a square either way.
      junk_type = common.randint(0, 1)  # The junk is always 2 on one side.
      junk_size = common.randint(2, 3) if min(wide, tall) > 4 else 2
      wides.append(2 if junk_type == 0 else junk_size)
      talls.append(2 if junk_type == 1 else junk_size)
      coin1, coin2 = common.randint(0, 1), common.randint(0, 1)
      rows.append(rows[i] + (0 if coin1 else talls[i] - talls[-1]))
      cols.append(cols[i] + (0 if coin2 else wides[i] - wides[-1]))
      colors.append(common.black())

  grid, output = common.grids(size, size)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        output[r][c] = grid[r][c] = common.gray()
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        grid[r][c] = common.black()
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 4, 4, 8, 9], cols=[1, 7, 9, 2, 2],
               wides=[4, 4, 2, 4, 3], talls=[4, 4, 2, 4, 3],
               colors=[2, 0, 0, 0, 2]),
      generate(rows=[1, 1, 3, 7, 8], cols=[1, 2, 6, 0, 0],
               wides=[4, 3, 6, 5, 4], talls=[4, 3, 6, 5, 4],
               colors=[0, 2, 2, 0, 2]),
      generate(rows=[1, 3, 8], cols=[1, 7, 3], wides=[5, 4, 6], talls=[6, 4, 4],
               colors=[0, 2, 0]),
      generate(rows=[1, 3, 6, 6], cols=[1, 1, 3, 6], wides=[4, 4, 5, 2],
               talls=[4, 2, 5, 3], colors=[0, 0, 0, 0]),
  ]
  test = [
      generate(rows=[1, 1, 1, 8], cols=[0, 7, 7, 2], wides=[5, 4, 2, 6],
               talls=[5, 5, 2, 4], colors=[2, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
