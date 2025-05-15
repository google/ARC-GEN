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


def generate(rows=None, cols=None, idxs=None, color=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of angles where the arrows are pointing
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_arrows, color = common.randint(2, 3), common.random_color()
    while True:
      rows = [common.randint(1, size - 3) for _ in range(num_arrows)]
      cols = [common.randint(1, size - 3) for _ in range(num_arrows)]
      idxs = [common.randint(0, 3) for _ in range(num_arrows)]
      overlaps = False
      for j in range(num_arrows):
        for i in range(num_arrows):
          if i == j: continue
          overlaps = overlaps or idxs[i] == idxs[j]  # avoid the same angles
          ir, ic = -1 if idxs[i] in [0,1] else 1, -1 if idxs[i] in [0,2] else 1
          jr, jc = -1 if idxs[j] in [0,1] else 1, -1 if idxs[j] in [0,2] else 1
          overlaps = overlaps or (ic == jc and ir < jr and rows[i] > rows[j])
          overlaps = overlaps or (ir == jr and ic < jc and cols[i] > cols[j])
          if ic != jc and ir != jr:  # potential collision
            if ir < jr and ic < jc:
              overlaps = overlaps or (rows[i] > rows[j] and cols[i] > cols[j])
            if ir < jr and ic > jc:
              overlaps = overlaps or (rows[i] > rows[j] and cols[i] < cols[j])
          if abs(rows[i] - rows[j]) < 4 and abs(cols[i] - cols[j]) < 4:
            overlaps = True
      if not overlaps: break

  grid, output = common.grids(size, size)
  for r, c, idx in zip(rows, cols, idxs):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      output[r + dr][c + dc] = grid[r + dr][c + dc] = color
    dr, dc = -1 if idx in [0, 1] else 1, -1 if idx in [0, 2] else 1
    r, c = r if dr == -1 else r + 1, c if dc == -1 else c + 1
    grid[r][c] = output[r][c] = common.black()
    while True:
      r, c = r + dr, c + dc
      if r < 0 or r >= size or c < 0 or c >= size: break
      output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 4], cols=[1, 6], idxs=[1, 2], color=7),
      generate(rows=[1, 6], cols=[3, 3], idxs=[2, 1], color=9),
  ]
  test = [
      generate(rows=[2, 4, 6], cols=[3, 7, 2], idxs=[0, 3, 2], color=8),
  ]
  return {"train": train, "test": test}
