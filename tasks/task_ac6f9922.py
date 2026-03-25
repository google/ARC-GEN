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


def generate(size=None, width=None, height=None, row_offset=None,
             col_offset=None, bgcolor=None, fgcolor=None, wides=None,
             talls=None, brows=None, bcols=None, colors=None, lengths=None,
             flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    width: The width of the grid.
    height: The height of the grid.
    row_offset: The row offset of the grid.
    col_offset: The col offset of the grid.
    bgcolor: The background color of the grid.
    fgcolor: The foreground color of the grid.
    wides: The widths of the inner grids.
    talls: The heights of the inner grids.
    brows: The row offsets of the inner grids.
    bcols: The col offsets of the inner grids.
    colors: The colors of the inner grids.
    lengths: The lengths of the inner grids.
    flip: Whether to flip the grid.
  """

  if size is None:
    while True:
      wides = [common.randint(3, 6) for _ in range(common.randint(2, 3))]
      talls = [common.randint(3, 6) for _ in range(common.randint(2, 3))]
      width = sum(wides) + len(wides) + 1 + common.randint(0, 3)
      height = sum(talls) + len(talls) + 1 + common.randint(0, 3)
      if abs(width - height) <= 2: break
    size = max(width, height) + common.randint(2, 4)
    while True:
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      if brows != sorted(brows): continue
      if not common.overlaps_1d(brows, talls, 1): break
    while True:
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      if bcols != sorted(bcols): continue
      if not common.overlaps_1d(bcols, wides, 1): break
    row_offset = common.randint(1, size - height - 1)
    col_offset = common.randint(1, size - width - 1)
    subset = common.shuffle(list(range(1, 10)))
    bgcolor = subset.pop()
    fgcolor = subset.pop()
    colors = [common.randint(0, 1) for _ in range(len(wides) * len(talls))]
    colors = [bgcolor if color else common.choice(subset) for color in colors]
    lengths = []
    for tall in talls:
      for _ in wides:
        lengths.append(common.randint(1, tall - 2))
    flip = common.randint(0, 1)

  grid = common.grid(size, size, bgcolor)
  output = common.grid(len(wides), len(talls))
  common.rect(grid, width, height, row_offset, col_offset, fgcolor)
  for row, (tall, brow) in enumerate(zip(talls, brows)):
    for col, (wide, bcol) in enumerate(zip(wides, bcols)):
      color = colors[row * len(wides) + col]
      length = lengths[row * len(wides) + col]
      common.rect(grid, wide, tall, row_offset + brow, col_offset + bcol, bgcolor)
      common.rect(grid, wide - 2, length, row_offset + brow + 1, col_offset + bcol + 1, color)
      output[row][col] = color
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=17, width=14, height=15, row_offset=1, col_offset=1,
               bgcolor=8, fgcolor=1, wides=[4, 4], talls=[6, 4], brows=[2, 9],
               bcols=[2, 7], colors=[3, 8, 8, 2], lengths=[2, 2, 2, 2], flip=1),
      generate(size=13, width=11, height=11, row_offset=1, col_offset=1,
               bgcolor=4, fgcolor=1, wides=[4, 3], talls=[4, 3], brows=[2, 7],
               bcols=[2, 7], colors=[2, 4, 4, 4], lengths=[2, 1, 1, 1], flip=0),
      generate(size=17, width=15, height=15, row_offset=1, col_offset=1,
               bgcolor=1, fgcolor=2, wides=[3, 4, 3], talls=[6, 5],
               brows=[1, 9], bcols=[1, 5, 10], colors=[3, 4, 1, 1, 6, 8],
               lengths=[3, 2, 1, 1, 3, 3], flip=0),
  ]
  test = [
      generate(size=19, width=15, height=17, row_offset=1, col_offset=2,
               bgcolor=8, fgcolor=3, wides=[3, 4, 3], talls=[3, 5, 3],
               brows=[1, 5, 12], bcols=[1, 5, 11],
               colors=[2, 6, 1, 8, 4, 7, 8, 8, 1],
               lengths=[1, 1, 1, 1, 1, 3, 1, 1, 1], flip=0),
  ]
  return {"train": train, "test": test}
