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


def generate(arows=None, acols=None, brows=None, bcols=None, crows=None,
             ccols=None, rows=None, cols=None, width=10, height=15):
  """Returns input and output grids according to the given parameters.

  Args:
    arows: a list of vertical coordinates where A pixels should be placed
    acols: a list of horizontal coordinates where A pixels should be placed
    brows: a list of vertical coordinates where B pixels should be placed
    bcols: a list of horizontal coordinates where B pixels should be placed
    crows: a list of vertical coordinates where C pixels should be placed
    ccols: a list of horizontal coordinates where C pixels should be placed
    rows: a list of vertical coordinates where patterns should be placed
    cols: a list of horizontal coordinates where patterns should be placed
    width: the width of the grid
    height: the height of the grid
  """
  if arows is None:
    tall = min(3, common.randint(1, 5))
    awide = common.randint(1, 2)
    bwide = common.randint(1, 2)
    cwide = common.randint(1, 2)
    apixels = common.all_pixels(awide, tall)
    bpixels = common.all_pixels(bwide, tall)
    cpixels = common.all_pixels(cwide, tall)
    apixels = common.sample(apixels, common.randint(1, len(apixels)))
    bpixels = common.sample(bpixels, common.randint(1, len(bpixels)))
    cpixels = common.sample(cpixels, common.randint(1, len(cpixels)))
    arows, acols = zip(*apixels)
    brows, bcols = zip(*bpixels)
    crows, ccols = zip(*cpixels)
    rows, cols, r = [], [], common.randint(1, 2)
    while r + tall < height:
      rows.append(r)
      cols.append(awide * common.randint(1, 2))
      r += common.randint(tall + 1, tall + 3)

  grid, output = common.grids(width, height)
  awide, bwide, cwide = max(acols) + 1, max(bcols) + 1, max(ccols) + 1
  for idx in range(len(rows)):
    row, col = rows[idx], cols[idx]
    for c in range(0, col, awide):
      for ar, ac in zip(arows, acols):
        output[row + ar][c + ac] = grid[row + ar][c + ac] = common.cyan()
    for br, bc in zip(brows, bcols):
      output[row + br][col + bc] = grid[row + br][col + bc] = common.cyan()
    for c in range(col + bwide, width, cwide):
      for cr, cc in zip(crows, ccols):
        if not idx:
          common.draw(grid, row + cr, c + cc, common.cyan())
          common.draw(output, row + cr, c + cc, common.cyan())
        else:
          common.draw(output, row + cr, c + cc, common.blue())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(arows=[0], acols=[0], brows=[1], bcols=[0], crows=[2], ccols=[0],
               rows=[1, 6, 10], cols=[2, 3, 2]),
      generate(arows=[0], acols=[0], brows=[0], bcols=[0], crows=[0], ccols=[0],
               rows=[2, 6, 11, 13], cols=[2, 2, 3, 1]),
      generate(arows=[0, 1], acols=[0, 1], brows=[0], bcols=[0], crows=[0, 1],
               ccols=[1, 0], rows=[1, 6, 10], cols=[2, 2, 4]),
  ]
  test = [
      generate(arows=[1], acols=[0], brows=[0, 0, 2, 2], bcols=[0, 1, 0, 1],
               crows=[0, 2], ccols=[0, 0], rows=[1, 8], cols=[2, 3]),
  ]
  return {"train": train, "test": test}
