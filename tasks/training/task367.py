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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, arows=None, acols=None, zrows=None, zcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of vertical coordinates where boxes should be placed
    talls: a list of horizontal coordinates where boxes should be placed
    arows: a list of vertical coordinates where lines should start
    acols: a list of horizontal coordinates where lines should start
    zrows: a list of vertical coordinates where lines should end
    zcols: a list of horizontal coordinates where lines should end
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    num_boxes = common.randint(2, 4)
    # First, choose a nonoverlapping set of boxes.
    while True:
      wides = [common.randint(3, 7) for _ in range(num_boxes)]
      talls = [common.randint(3, 7) for _ in range(num_boxes)]
      rows = [common.randint(0, height - tall) for tall in talls]
      cols = [common.randint(-1, width - wide + 1) for wide in wides]
      overlaps = False
      for j in range(num_boxes):
        for i in range(j):
          if rows[i] + talls[i] < rows[j] or rows[j] + talls[j] < rows[i]:
            continue
          if cols[i] + wides[i] < cols[j] or cols[j] + wides[j] < cols[i]:
            continue
          overlaps = True
      if not overlaps: break
    # Second, draw them onto a bitmap (using '1' for each box cell)
    bitmap = common.grid(width, height, 0)
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          common.draw(bitmap, r, c, 1)
    # Third, try to connect pairs of boxes with lines.
    arows, acols, zrows, zcols = [], [], [], []
    for i in range(num_boxes):
      for j in range(num_boxes):
        if cols[i] < cols[j]:
          lorow = max(rows[i], rows[j]) + 1
          hirow = min(rows[i] + talls[i], rows[j] + talls[j]) - 2
          if lorow > hirow: continue
          row = common.randint(lorow, hirow)
          overlaps = False
          for c in range(cols[i] + wides[i], cols[j]):
            overlaps = overlaps or common.get_pixel(bitmap, row - 1, c) == 1
            overlaps = overlaps or common.get_pixel(bitmap, row, c) == 1
            overlaps = overlaps or common.get_pixel(bitmap, row + 1, c) == 1
          if overlaps or not common.randint(0, 3): continue
          if row > 0 and row + 1 < height:
            arows.append(row)
            acols.append(cols[i] + wides[i])
            zrows.append(row)
            zcols.append(cols[j] - 1)
        if rows[i] < rows[j]:
          locol = max(cols[i], cols[j]) + 1
          hicol = min(cols[i] + wides[i], cols[j] + wides[j]) - 2
          if locol > hicol: continue
          col = common.randint(locol, hicol)
          overlaps = False
          for r in range(rows[i] + talls[i], rows[j]):
            overlaps = overlaps or common.get_pixel(bitmap, r, col - 1) == 1
            overlaps = overlaps or common.get_pixel(bitmap, r, col) == 1
            overlaps = overlaps or common.get_pixel(bitmap, r, col + 1) == 1
          if overlaps or not common.randint(0, 3): continue
          if col > 0 and col + 1 < width:
            arows.append(rows[i] + talls[i])
            acols.append(col)
            zrows.append(rows[j] - 1)
            zcols.append(col)
    # Fourth, try to connect boxes to the edge of the bitmap.
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      if row > 0 and col >= 0 and col + wide < width:
        c = common.randint(col + 1, col + wide - 2)
        overlaps = False
        for r in range(0, row):
          overlaps = overlaps or common.get_pixel(bitmap, r, c - 1) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r, c) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r, c + 1) == 1
        if overlaps or not common.randint(0, 3): continue
        arows.append(0)
        acols.append(c)
        zrows.append(row - 1)
        zcols.append(c)
      if col > 0 and row >= 0 and row + tall < height:
        r = common.randint(row + 1, row + tall - 2)
        overlaps = False
        for c in range(0, col):
          overlaps = overlaps or common.get_pixel(bitmap, r - 1, c) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r, c) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r + 1, c) == 1
        if overlaps or not common.randint(0, 3): continue
        arows.append(r)
        acols.append(0)
        zrows.append(r)
        zcols.append(col - 1)
      if row + tall < height and col >= 0 and col + wide < width:
        c = common.randint(col + 1, col + wide - 2)
        overlaps = False
        for r in range(row + tall, height):
          overlaps = overlaps or common.get_pixel(bitmap, r, c - 1) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r, c) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r, c + 1) == 1
        if overlaps or not common.randint(0, 3): continue
        arows.append(row + tall)
        acols.append(c)
        zrows.append(height - 1)
        zcols.append(c)
      if col + wide < width and row >= 0 and row + tall < height:
        r = common.randint(row + 1, row + tall - 2)
        overlaps = False
        for c in range(col + wide, width):
          overlaps = overlaps or common.get_pixel(bitmap, r - 1, c) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r, c) == 1
          overlaps = overlaps or common.get_pixel(bitmap, r + 1, c) == 1
        if overlaps or not common.randint(0, 3): continue
        arows.append(r)
        acols.append(col + wide)
        zrows.append(r)
        zcols.append(width - 1)

  grid, output = common.grids(width, height)
  for row, col, wide, tall in zip(rows, cols, wides, talls):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        common.draw(grid, r, c, common.gray())
        common.draw(output, r, c, common.gray())
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        common.draw(grid, r, c, common.black())
        common.draw(output, r, c, common.yellow())
    for arow, acol, zrow, zcol in zip(arows, acols, zrows, zcols):
      r, c = arow, acol
      dr, dc = (0 if arow == zrow else 1, 0 if acol == zcol else 1)
      while True:
        common.draw(grid, r, c, common.gray())
        common.draw(output, r, c, common.gray())
        if r == zrow and c == zcol: break
        r, c = r + dr, c + dc
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=12, rows=[1, 1, 5, 0], cols=[-1, 5, 11, 17],
               wides=[3, 4, 4, 3], talls=[3, 7, 4, 5], arows=[2, 2, 0, 7, 9, 8],
               acols=[2, 9, 13, 15, 13, 6], zrows=[2, 2, 4, 7, 11, 11],
               zcols=[4, 16, 13, 18, 13, 6]),
      generate(width=16, height=13, rows=[4, 4], cols=[3, 14], wides=[5, 3],
               talls=[5, 5], arows=[6, 11, 0, 9, 0], acols=[8, 0, 5, 5, 11],
               zrows=[6, 11, 3, 12, 5], zcols=[13, 4, 5, 5, 11]),
      generate(width=17, height=15, rows=[1, 4, 10], cols=[11, 3, 10],
               wides=[5, 4, 4], talls=[5, 5, 4],
               arows=[2, 5, 11, 3, 0, 9, 6, 14],
               acols=[0, 0, 0, 16, 5, 5, 12, 12],
               zrows=[2, 5, 11, 3, 3, 14, 9, 14],
               zcols=[10, 2, 9, 16, 5, 5, 12, 12]),
  ]
  test = [
      generate(width=18, height=16, rows=[2, 7, 8, 13], cols=[-1, 13, 5, 0],
               wides=[4, 4, 5, 3], talls=[3, 5, 4, 3],
               arows=[3, 9, 9, 9, 10, 0, 12, 4],
               acols=[3, 0, 10, 17, 1, 7, 7, 14],
               zrows=[3, 9, 9, 9, 12, 7, 15, 6],
               zcols=[17, 4, 12, 17, 1, 7, 7, 14]),
  ]
  return {"train": train, "test": test}
