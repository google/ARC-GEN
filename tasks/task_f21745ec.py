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


def generate(width=None, height=None, brows=None, bcols=None, wides=None,
             talls=None, colors=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    colors: The colors of the boxes.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
  """

  if width is None:
    width = common.randint(19, 22)
    height = width + common.randint(0, 2) - 1
    copies = common.randint(2, 3)
    noncopies = common.randint(1, 3)
    while True:
      wide, tall = common.randint(4, 10), common.randint(4, 10)
      wides, talls = [wide] * copies, [tall] * copies
      for _ in range(noncopies):
        while True:
          w, t = common.randint(4, 10), common.randint(4, 10)
          if w == wide and t == tall: continue
          wides.append(w)
          talls.append(t)
          break
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    while True:
      pixels = common.random_pixels(wides[0] - 2, talls[0] - 2)
      if not pixels: continue
      rows, cols = zip(*pixels)
      break
    colors = common.random_colors(copies + noncopies)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    brow, bcol, wide, tall = brows[i], bcols[i], wides[i], talls[i]
    common.hollow_rect(grid, wide, tall, brow, bcol, color)
    if i == 0:
      for row, col in zip(rows, cols):
        grid[brow + 1 + row][bcol + 1 + col] = color
    if wide == wides[0] and tall == talls[0]:
      common.hollow_rect(output, wide, tall, brow, bcol, color)
      for row, col in zip(rows, cols):
        output[brow + 1 + row][bcol + 1 + col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=21, brows=[11, 2, 7, 1, 16],
               bcols=[11, 16, 1, 7, 3], wides=[5, 5, 5, 5, 5],
               talls=[6, 6, 6, 6, 4], colors=[5, 2, 4, 3, 7],
               rows=[0, 1, 1, 2, 2, 3], cols=[1, 0, 1, 1, 2, 0]),
      generate(width=19, height=19, brows=[1, 2, 11, 11], bcols=[1, 11, 3, 13],
               wides=[8, 8, 8, 5], talls=[7, 7, 7, 5], colors=[8, 6, 4, 5],
               rows=[0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4],
               cols=[5, 1, 2, 0, 1, 3, 4, 2, 3, 5, 4]),
      generate(width=22, height=22, brows=[8, 3, 1, 12, 15],
               bcols=[0, 16, 5, 11, 2], wides=[7, 4, 7, 7, 6],
               talls=[6, 4, 6, 6, 7], colors=[8, 3, 2, 1, 7],
               rows=[0, 1, 1, 1, 1, 2, 2, 2, 2, 3],
               cols=[1, 0, 1, 3, 4, 1, 2, 3, 4, 3]),
  ]
  test = [
      generate(width=22, height=23, brows=[12, 1, 8, 2, 14, 18],
               bcols=[1, 12, 11, 2, 15, 4], wides=[8, 10, 8, 8, 6, 9],
               talls=[5, 6, 5, 5, 6, 4], colors=[7, 8, 1, 5, 6, 3],
               rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               cols=[1, 2, 5, 0, 1, 3, 4, 5, 1, 2, 3]),
  ]
  return {"train": train, "test": test}
