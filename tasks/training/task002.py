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


def generate(size=None, rows=None, cols=None, brows=None, bcols=None,
             wides=None, talls=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where static should be placed
    cols: a list of horizontal coordinates where static should be placed
    brows: a list of vertical coordinates where the pots should be placed
    bcols: a list of horizontal coordinates where the pots should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
  """
  if size is None:
    num_pots = common.randint(1, 8)
    while True:
      size = common.randint(6, 20)
      wides = [common.randint(3, 8) for _ in range(num_pots)]
      talls = [common.randint(3, 8) for _ in range(num_pots)]
      if max(wides) > size or max(talls) > size: continue
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, -1): break
    while True:
      pixels = common.random_pixels(size, size, 0.05)
      if pixels: break
    rows, cols = zip(*pixels)

  grid, output = common.grids(size, size)
  # Draw the static.
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.green()
  # Draw the honey pots.
  for brow, bcol, wide, tall in zip(brows, bcols, wides, talls):
    for bitmap in [grid, output]:
      for r in range(1, tall - 1):
        for c in [0, wide - 1]:
          bitmap[brow + r][bcol + c] = common.green()
      for r in [0, tall - 1]:
        for c in range(1, wide - 1):
          bitmap[brow + r][bcol + c] = common.green()
    for r in range(1, tall - 1):
      for c in range(1, wide - 1):
        grid[brow + r][bcol + c] = common.black()
        output[brow + r][bcol + c] = common.yellow()
  # Finally, fill any cells that are surrounded.
  for r in range(size):
    for c in range(size):
      if output[r][c] == common.black() and common.is_surrounded(output, r, c):
        output[r][c] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=6, rows=[], cols=[], brows=[1, 2], bcols=[1, 2],
               wides=[3, 3], talls=[3, 3]),
      generate(size=10, rows=[1, 1, 2, 2, 3, 5, 5, 6, 6, 6, 7],
               cols=[2, 4, 3, 5, 2, 3, 5, 2, 3, 4, 3], brows=[3], bcols=[5],
               wides=[3], talls=[3]),
      generate(size=10, rows=[0, 1, 2, 2, 3, 7, 8], cols=[5, 4, 1, 2, 0, 7, 8],
               brows=[2, 2], bcols=[3, 6], wides=[4, 3], talls=[6, 3]),
      generate(size=10, rows=[1, 1, 3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 7],
               cols=[2, 5, 7, 2, 5, 6, 7, 8, 3, 8, 3, 7, 3], brows=[1, 6, 7],
               bcols=[2, 7, 3], wides=[4, 3, 3], talls=[4, 3, 3]),
      generate(size=20,
               rows=[2, 2, 2, 2, 3, 4, 4, 6, 9, 9, 9, 10, 11, 11, 11, 12, 12,
                     13, 13, 13, 14, 14, 14, 14, 14, 15, 16, 16, 16, 17],
               cols=[4, 5, 6, 10, 18, 8, 15, 4, 2, 8, 15, 8, 10, 15, 17, 6, 13,
                     11, 14, 17, 7, 10, 12, 15, 17, 10, 12, 15, 17, 13],
               brows=[1, 2, 4, 11, 14], bcols=[7, 8, 8, 7, 15],
               wides=[3, 3, 8, 4, 3], talls=[3, 3, 6, 4, 3]),
  ]
  test = [
      generate(size=20,
               rows=[2, 3, 5, 5, 6, 6, 9, 11, 12, 12, 12, 13, 15, 15, 15, 15,
                     18, 18],
               cols=[4, 4, 4, 12, 13, 17, 9, 9, 6, 13, 17, 9, 4, 6, 7, 11, 7,
                     11],
               brows=[1, 3, 3, 6, 9, 11, 13, 15],
               bcols=[1, 4, 9, 13, 9, 7, 1, 7], wides=[3, 6, 4, 5, 5, 3, 3, 5],
               talls=[3, 3, 3, 7, 3, 3, 3, 4]),
  ]
  return {"train": train, "test": test}
