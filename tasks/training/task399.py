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


def generate(size=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if size is None:
    size = common.randint(3, 7)
    num_boxes = 1
    if size == 5: num_boxes = common.randint(1, 2)
    if size == 6: num_boxes = common.randint(2, 3)
    if size == 7: num_boxes = common.randint(3, 5)
    while True:
      rows = [common.randint(0, size - 2) for _ in range(num_boxes)]
      cols = [common.randint(0, size - 2) for _ in range(num_boxes)]
      overlaps = False  # Special overlap logic
      for j in range(num_boxes):
        for i in range(j):
          if abs(rows[j] - rows[i]) > 1 and abs(cols[j] - cols[i]) > 1:
            continue
          if abs(rows[j] - rows[i]) > 2 or abs(cols[j] - cols[i]) > 2:
            continue
          overlaps = True
      if not overlaps: break

  grid, output = common.grid(size, size), common.grid(3, 3)
  for row, col in zip(rows, cols):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      grid[row + dr][col + dc] = common.red()
  if len(rows) >= 1: output[0][0] = common.blue()
  if len(rows) >= 2: output[0][2] = common.blue()
  if len(rows) >= 3: output[1][1] = common.blue()
  if len(rows) >= 4: output[2][0] = common.blue()
  if len(rows) >= 5: output[2][2] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[0], cols=[0]),
      generate(size=5, rows=[1, 3], cols=[1, 3]),
      generate(size=7, rows=[1, 2, 4], cols=[1, 4, 2]),
      generate(size=6, rows=[1, 4], cols=[1, 2]),
      generate(size=3, rows=[1], cols=[1]),
      generate(size=7, rows=[0, 2, 3, 5], cols=[4, 1, 4, 1]),
      generate(size=7, rows=[0, 1, 3, 4, 5], cols=[4, 1, 5, 0, 3]),
      generate(size=7, rows=[0, 0, 2, 3], cols=[2, 5, 0, 3]),
  ]
  test = [
      generate(size=6, rows=[0, 1, 3], cols=[3, 0, 2]),
      generate(size=7, rows=[1, 1, 3, 4], cols=[0, 3, 5, 2]),
      generate(size=7, rows=[0, 0, 2, 3, 5], cols=[0, 3, 5, 1, 4]),
  ]
  return {"train": train, "test": test}
