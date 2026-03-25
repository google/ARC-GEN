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


def generate(rows=None, cols=None, idxs=None, horizon=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of 0/1 values (for blue/red pixels, respectively)
    horizon: the placement of the grey horizon
    size: the width and height of the (square) grid
  """
  if rows is None:
    horizon = common.randint(3, 6)
    rows, cols = [], []
    for c in range(size):
      if common.randint(0, 1) == 0: continue
      rows.append(common.randint(0, horizon - 2))
      cols.append(c)
    for c in range(size):
      if common.randint(0, 1) == 0: continue
      rows.append(common.randint(horizon + 2, size - 1))
      cols.append(c)
    idxs = [common.randint(0, 1) for _ in range(len(rows))]

  grid, output = common.grids(size, size)
  for c in range(size):
    output[horizon][c] = grid[horizon][c] = common.gray()
  for r, c, idx in zip(rows, cols, idxs):
    grid[r][c] = idx + 1
    dr = -1 if idx == 0 else 1
    dr = dr if r < horizon else -dr
    while True:
      if r < 0 or r >= size or output[r][c]:
        break
      output[r][c], r = idx + 1, r + dr
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2, 2, 8, 8, 8], cols=[2, 6, 1, 9, 1, 5, 8],
               idxs=[0, 0, 1, 1, 0, 1, 0], horizon=5),
      generate(rows=[0, 0, 1, 1, 5, 5, 6, 8, 8, 8],
               cols=[1, 3, 5, 7, 1, 9, 4, 2, 6, 8],
               idxs=[1, 0, 1, 0, 1, 1, 0, 0, 1, 0], horizon=3),
  ]
  test = [
      generate(rows=[1, 1, 1, 2, 7, 7, 8, 9], cols=[1, 3, 8, 6, 2, 5, 0, 8],
               idxs=[1, 0, 1, 0, 0, 1, 1, 0], horizon=4),
  ]
  return {"train": train, "test": test}
