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


def generate(rows=None, cols=None, wides=None, talls=None, flip=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths for the boxes
    talls: a list of heights for the boxes
    flip: whether to flip the boxes vertically
    size: the width and height of the (square) grid
  """
  if rows is None:
    # Choose the # of boxes and their boundaries (e.g., the whole grid if 1 box)
    num_boxes = common.randint(1, 2)
    lengths, depths = [size], [size]
    if num_boxes == 2:
      row, col = common.randint(4, 6), common.randint(4, 6)
      lengths, depths = [col, size - col], [row, size - row]
    # Place the boxes within their respective quadrants.
    rows, cols, wides, talls = [], [], [], []
    for idx in range(num_boxes):
      length, depth = lengths[idx], depths[idx]
      wide = common.randint(3, min(6, length))
      tall = common.randint(3, min(6, depth))
      row = sum(depths[:idx]) + common.randint(0, depth - tall)
      col = sum(lengths[:idx]) + common.randint(0, length - wide)
      rows.append(row)
      cols.append(col)
      wides.append(wide)
      talls.append(tall)
    flip = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for dr, dc in [(0, 0), (0, wide - 1), (tall - 1, 0), (tall - 1, wide - 1)]:
      output[row + dr][col + dc] = grid[row + dr][col + dc] = common.yellow()
    for dr in range(1, tall - 1):
      for dc in range(1, wide - 1):
        output[row + dr][col + dc] = common.red()
  if flip: grid, output = grid[::-1], output[::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3], cols=[3], wides=[3], talls=[3], flip=0),
      generate(rows=[1], cols=[1], wides=[6], talls=[6], flip=0),
      generate(rows=[1, 6], cols=[1, 4], wides=[3, 6], talls=[3, 4], flip=0),
  ]
  test = [
      generate(rows=[1, 5], cols=[0, 5], wides=[4, 5], talls=[4, 5], flip=1),
  ]
  return {"train": train, "test": test}
