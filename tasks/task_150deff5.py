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


def generate(width=None, height=None, rows=None, cols=None, idxs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where toys should be placed
    cols: a list of horizontal coordinates where toys should be placed
    idxs: a list of toy indices (0=box, 1=tall stick, 2=flat stick)
  """
  if width is None:
    width, height = common.randint(9, 11), common.randint(8, 9)
    num_boxes = 2 if width < 10 else 3
    while True:
      brows = [common.randint(1, 5) for _ in range(num_boxes)]
      bcols = [common.randint(1, 6) for _ in range(num_boxes)]
      bidxs = [0] * num_boxes
      # Check that no two boxes are alongside + parallel to each other.
      parallel = False
      for j in range(num_boxes):
        for i in range(j):
          if brows[i] == brows[j] and abs(bcols[i] - bcols[j]) <= 2:
            parallel = True
          if bcols[i] == bcols[j] and abs(brows[i] - brows[j]) <= 2:
            parallel = True
      if parallel: continue
      bwides, btalls = [2] * num_boxes, [2] * num_boxes
      if not common.overlaps(brows, bcols, bwides, btalls): break
    if common.randint(0, 1): num_boxes += 1
    while True:
      srows = [common.randint(1, 5) for _ in range(num_boxes)]
      scols = [common.randint(1, 6) for _ in range(num_boxes)]
      sidxs = [common.randint(1, 2) for _ in range(num_boxes)]
      # Check that no two sticks are alongside + parallel to each other.
      parallel = False
      for j in range(num_boxes):
        for i in range(j):
          if sidxs[i] != sidxs[j]: continue
          if srows[i] == srows[j] and abs(scols[i] - scols[j]) <= 1:
            parallel = True
          if scols[i] == scols[j] and abs(srows[i] - srows[j]) <= 1:
            parallel = True
      if parallel: continue
      swides = [1 if idx == 1 else 3 for idx in sidxs]
      stalls = [3 if idx == 1 else 1 for idx in sidxs]
      if not common.overlaps(brows + srows, bcols + scols, bwides + swides,
                             btalls + stalls): break
    rows = brows + srows
    cols = bcols + scols
    idxs = bidxs + sidxs

  grid, output = common.grids(width, height)
  for row, col, idx in zip(rows, cols, idxs):
    if idx == 0:
      for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        grid[row + dr][col + dc] = common.gray()
        output[row + dr][col + dc] = common.cyan()
    if idx == 1:
      for dr, dc in [(0, 0), (1, 0), (2, 0)]:
        grid[row + dr][col + dc] = common.gray()
        output[row + dr][col + dc] = common.red()
    if idx == 2:
      for dr, dc in [(0, 0), (0, 1), (0, 2)]:
        grid[row + dr][col + dc] = common.gray()
        output[row + dr][col + dc] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=9, rows=[1, 3, 4, 3, 2, 6],
               cols=[2, 4, 6, 3, 4, 5], idxs=[0, 0, 0, 1, 2, 2]),
      generate(width=10, height=8, rows=[1, 1, 4, 1, 1, 4],
               cols=[1, 4, 5, 3, 6, 4], idxs=[0, 0, 0, 1, 1, 1]),
      generate(width=9, height=8, rows=[1, 4, 1, 3], cols=[4, 4, 1, 3],
               idxs=[0, 0, 2, 1]),
  ]
  test = [
      generate(width=11, height=8, rows=[0, 2, 5, 0, 2, 4, 1],
               cols=[2, 4, 5, 5, 1, 3, 6], idxs=[0, 0, 0, 2, 2, 2, 1]),
  ]
  return {"train": train, "test": test}
