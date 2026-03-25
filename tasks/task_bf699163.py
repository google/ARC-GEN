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


def generate(width=None, height=None, brows=None, bcols=None, bcolors=None,
             prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    brows: The row indices of the hollow rectangles.
    bcols: The column indices of the hollow rectangles.
    bcolors: The colors of the hollow rectangles.
    prows: The row indices of the pixels.
    pcols: The column indices of the pixels.
  """

  def draw():
    grid, output = common.grid(width, height, 5), common.grid(3, 3, 5)
    for brow, bcol, bcolor in zip(brows, bcols, bcolors):
      common.hollow_rect(grid, 3, 3, brow, bcol, bcolor)
    for prow, pcol in zip(prows, pcols):
      common.draw(grid, prow, pcol, 7)
    common.hollow_rect(output, 3, 3, 0, 0, bcolors[-1])
    return grid, output

  if width is None:
    height = common.randint(15, 20)
    width = height + common.randint(-1, 1)
    num_boxes = height // 3
    bcolors = common.random_colors(num_boxes, exclude=[5, 7])
    while True:
      brows = [common.randint(0, height - 3) for _ in range(num_boxes - 1)]
      bcols = [common.randint(0, width - 3) for _ in range(num_boxes - 1)]
      sizes = [3] * (num_boxes - 1)
      if common.overlaps(brows, bcols, sizes, sizes, 1): continue
      wide = common.randint(7, width // 2)
      tall = common.randint(7, height // 2)
      orow = common.randint(-1, height - tall + 1)
      ocol = common.randint(-1, width - wide + 1)
      if common.overlaps(brows + [orow], bcols + [ocol], sizes + [wide], sizes + [tall]):
        continue
      brows.append(common.randint(orow + 2, orow + tall - 5))
      bcols.append(common.randint(ocol + 2, ocol + wide - 5))
      prows, pcols = [], []
      for row in range(orow, orow + tall):
        for col in range(ocol, ocol + wide):
          if row in [orow, orow + tall - 1] or col in [ocol, ocol + wide - 1]:
            if common.randint(0, 3):
              prows.append(row)
              pcols.append(col)
      # Let's make sure the corner(s) are visibile.
      good = True
      grid, _ = draw()
      for row, col in [(orow, ocol),
                       (orow, ocol + wide - 1),
                       (orow + tall - 1, ocol),
                       (orow + tall - 1, ocol + wide - 1)]:
        if common.get_pixel(grid, row, col) == 5: good = False
      if not good: continue
      # Let's make sure that orange pixels occupy multiple rows and columns.
      visible_rows, visible_cols = [], []
      for row in range(height):
        for col in range(width):
          if grid[row][col] != 7: continue
          visible_rows.append(row)
          visible_cols.append(col)
      if len(set(visible_rows)) >= 2 and len(set(visible_cols)) >= 2: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=17, brows=[1, 4, 6, 14, 9],
               bcols=[2, 7, 14, 11, 3], bcolors=[1, 3, 2, 8, 4],
               prows=[7, 7, 7, 7, 7, 7, 8, 8, 9, 9, 11, 11, 12, 13, 14, 14, 15, 16, 16],
               pcols=[1, 2, 3, 5, 6, 7, 1, 7, 1, 7, 1, 7, 1, 1, 1, 7, 7, 1, 7]),
      generate(width=16, height=17, brows=[1, 2, 6, 13, 10],
               bcols=[1, 11, 4, 1, 10], bcolors=[8, 2, 3, 6, 1],
               prows=[8, 8, 8, 8, 8, 8, 9, 11, 12, 13, 14, 16],
               pcols=[8, 9, 10, 11, 14, 15, 8, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(width=14, height=13, brows=[1, 6, 10, 0], bcols=[2, 9, 3, 10],
               bcolors=[6, 8, 1, 2], prows=[0, 1, 2, 4, 4, 4, 4],
               pcols=[8, 8, 8, 8, 9, 12, 13]),
  ]
  return {"train": train, "test": test}
