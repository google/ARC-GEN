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


def generate(rows=None, cols=None, idxs=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of cell positions (0, 1, 2, or 3)
    colors: a list of colors for the four cell positions
  """
  if rows is None:
    colors = common.random_colors(4, exclude=[common.blue()])
    rows, cols, idxs = [], [], []
    for idx in [0, 3] if common.randint(0, 1) else [1, 2]:
      if common.randint(0, 1):  # Sometimes we'll do a subset of the corners
        if common.randint(0, 1):
          rows.append(0)
          cols.append(0)
          idxs.append(idx)
        if common.randint(0, 1):
          rows.append(0)
          cols.append(2)
          idxs.append(idx)
        if common.randint(0, 1):
          rows.append(2)
          cols.append(0)
          idxs.append(idx)
        if common.randint(0, 1):
          rows.append(2)
          cols.append(2)
          idxs.append(idx)
        continue
      if common.randint(0, 1):  # Sometimes we'll do left-to-right
        rows.append(1)
        cols.append(0)
        idxs.append(idx)
        rows.append(1)
        cols.append(2)
        idxs.append(idx)
        continue
      if common.randint(0, 1):  # Sometimes we'll do up-to-down
        rows.append(0)
        cols.append(1)
        idxs.append(idx)
        rows.append(2)
        cols.append(1)
        idxs.append(idx)

  grid, output = common.grids(8, 8, common.blue())
  # Mark the original cells, then infer new ones.
  origs = [1] * len(idxs)
  for j in range(len(idxs)):
    for i in range(j):
      if idxs[i] != idxs[j]: continue
      if rows[i] == rows[j]:
        rows.append(rows[i])
        cols.append(1)
        idxs.append(idxs[i])
        origs.append(0)
      if cols[i] == cols[j]:
        rows.append(1)
        cols.append(cols[i])
        idxs.append(idxs[i])
        origs.append(0)
  for r in range(8):
    for c in range(8):
      if r % 3 == 2 or c % 3 == 2: output[r][c] = grid[r][c] = common.black()
  for r, c, i, o in zip(rows, cols, idxs, origs):
    roff, coff = 0 if i in [0, 1] else 1, 0 if i in [0, 2] else 1
    if o: grid[3 * r + roff][3 * c + coff] = colors[i]
    output[3 * r + roff][3 * c + coff] = colors[i]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 2, 0], idxs=[1, 1, 2, 2, 1],
               colors=[1, 4, 2, 1]),
      generate(rows=[0, 0, 0, 2, 2], cols=[0, 1, 2, 1, 2], idxs=[3, 0, 3, 0, 3],
               colors=[7, 1, 1, 3]),
      generate(rows=[1, 1], cols=[0, 2], idxs=[2, 2], colors=[1, 1, 3, 1]),
  ]
  test = [
      generate(rows=[0, 0, 2, 2, 2], cols=[0, 2, 0, 2, 2], idxs=[3, 3, 0, 0, 3],
               colors=[6, 1, 1, 8]),
  ]
  return {"train": train, "test": test}
