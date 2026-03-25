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


def generate(rows=None, cols=None, boxrow=None, boxcol=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxrow: the row of the box
    boxcol: the column of the box
    size: the width and height of the (square) grid
  """
  if rows is None:
    boxrow, boxcol = common.randint(2, 6), common.randint(2, 6)
    rows, cols = [], []
    for r in range(-1, 3):
      for c in range(-1, 3):
        if (r in [0, 1] and c in [0, 1]) or common.randint(0, 1): continue
        max_len = size
        max_len = max_len if r > -1 else min(max_len, boxrow - 1)
        max_len = max_len if c > -1 else min(max_len, boxcol - 1)
        max_len = max_len if r < 2 else min(max_len, size - boxrow - 3)
        max_len = max_len if c < 2 else min(max_len, size - boxcol - 3)
        length = common.randint(1, max_len)
        dr = r - (0 if r > -1 else length) + (0 if r < 2 else length)
        dc = c - (0 if c > -1 else length) + (0 if c < 2 else length)
        rows.append(boxrow + dr)
        cols.append(boxcol + dc)

  grid, output = common.grids(size, size)
  for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    grid[boxrow + dr][boxcol + dc] = common.red()
    output[boxrow + dr][boxcol + dc] = common.red()
  for r, c in zip(rows, cols):
    grid[r][c] = common.gray()
    r = r if r >= boxrow else boxrow - 1
    r = r if r <= boxrow + 1 else boxrow + 2
    c = c if c >= boxcol else boxcol - 1
    c = c if c <= boxcol + 1 else boxcol + 2
    output[r][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 3, 7], cols=[3, 8, 7], boxrow=3, boxcol=3),
      generate(rows=[0, 3, 6, 8], cols=[8, 1, 9, 5], boxrow=2, boxcol=5),
  ]
  test = [
      generate(rows=[0, 1, 6, 9], cols=[2, 8, 7, 2], boxrow=6, boxcol=2),
  ]
  return {"train": train, "test": test}
