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


def generate(width=None, height=None, bwides=None, btalls=None, brows=None,
             bcols=None, dwides=None, dtalls=None, drows=None, dcols=None,
             groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bwides: The widths of the blue boxes.
    btalls: The heights of the blue boxes.
    brows: The rows of the blue boxes.
    bcols: The columns of the blue boxes.
    dwides: The widths of the red boxes.
    dtalls: The heights of the red boxes.
    drows: The rows of the red boxes.
    dcols: The columns of the red boxes.
    groups: The groups of the red boxes.
  """

  if width is None:
    width, height = common.randint(8, 16), common.randint(8, 16)
    if common.randint(0, 1):
      bwide = width // 2 + common.randint(0, 2) - 1
      bwides = [width - bwide, bwide]
      btalls = [height, height]
      brows = [0, 0]
      bcols = [0, bwides[0]] if common.randint(0, 1) else [bwides[1], 0]
    else:
      bwides = [width, width]
      btall = height // 2 - common.randint(0, 1)
      btalls = [height - btall, btall]
      brows = [0, btalls[0]] if common.randint(0, 1) else [btalls[1], 0]
      bcols = [0, 0]
    while True:
      dwides, dtalls, drows, dcols, groups = [], [], [], [], []
      bad = False
      for group in [0, 1]:
        rows, talls = [], []
        row = common.randint(1, 2)
        while True:
          tall = common.randint(1, 4)
          if row + tall > btalls[group]: break
          rows.append(brows[group] + row)
          talls.append(tall)
          row += tall + common.randint(0, 2)
        max_wide = min(4, bwides[group] - 1)
        wides = [common.randint(1, max_wide) for _ in talls]
        cols = [bcols[group] + common.randint(0, bwides[group] - wide) for wide in wides]
        # Make sure that the red rectangles within this group are not touching.
        for i in range(1, len(wides)):
          if rows[i - 1] + talls[i - 1] < rows[i]: continue
          if cols[i - 1] + wides[i - 1] < cols[i]: continue
          if cols[i] + wides[i] < cols[i - 1]: continue
          bad = True
        drows.extend(rows)
        dcols.extend(cols)
        dwides.extend(wides)
        dtalls.extend(talls)
        groups.extend([group for _ in talls])
      if bad: continue  # we had a pair of red rectangles touching.
      if groups.count(0) < 2 or groups.count(1) < 2: continue  # need 2 per group
      break

  grid, output = common.grids(width, height)
  for group in [0, 1]:
    bwide, btall, brow, bcol = bwides[group], btalls[group], brows[group], bcols[group]
    common.rect(grid, bwide, btall, brow, bcol, 8 if group else 1)
    common.rect(output, bwide, btall, brow, bcol, 8 if group else 1)
  for dwide, dtall, drow, dcol, group in zip(dwides, dtalls, drows, dcols, groups):
    common.rect(grid, dwide, dtall, drow, dcol, 2)
    col = bcols[group] + (0 if group else (bwides[group] - dwide))
    common.rect(output, dwide, dtall, drow, col, 2)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, bwides=[11, 11], btalls=[4, 8],
               brows=[8, 0], bcols=[0, 0], dwides=[2, 3, 2, 1],
               dtalls=[2, 2, 2, 1], drows=[2, 5, 9, 11], dcols=[2, 5, 3, 8],
               groups=[1, 1, 0, 0]),
      generate(width=13, height=11, bwides=[7, 6], btalls=[11, 11],
               brows=[0, 0], bcols=[0, 7], dwides=[2, 2, 3, 2],
               dtalls=[3, 2, 2, 2], drows=[1, 3, 6, 8], dcols=[9, 2, 2, 8],
               groups=[1, 0, 0, 1]),
      generate(width=14, height=12, bwides=[8, 6], btalls=[12, 12],
               brows=[0, 0], bcols=[6, 0], dwides=[2, 2, 3, 2, 2],
               dtalls=[4, 2, 2, 2, 1], drows=[2, 2, 6, 7, 9],
               dcols=[2, 10, 8, 1, 11], groups=[1, 0, 0, 1, 0]),
      generate(width=15, height=15, bwides=[15, 15], btalls=[9, 6],
               brows=[0, 9], bcols=[0, 0], dwides=[2, 3, 1, 3],
               dtalls=[2, 2, 1, 2], drows=[2, 5, 10, 11], dcols=[3, 7, 2, 7],
               groups=[0, 0, 1, 1]),
  ]
  test = [
      generate(width=9, height=9, bwides=[9, 9], btalls=[4, 5], brows=[0, 4],
               bcols=[0, 0], dwides=[2, 1, 2, 1], dtalls=[1, 1, 2, 1],
               drows=[1, 2, 5, 7], dcols=[2, 5, 4, 1], groups=[0, 0, 1, 1]),
      generate(width=11, height=10, bwides=[6, 5], btalls=[10, 10],
               brows=[0, 0], bcols=[0, 6], dwides=[1, 2, 2, 4, 1],
               dtalls=[1, 2, 2, 2, 2], drows=[1, 3, 3, 6, 7],
               dcols=[7, 1, 8, 0, 8], groups=[1, 0, 1, 0, 1]),
  ]
  return {"train": train, "test": test}
