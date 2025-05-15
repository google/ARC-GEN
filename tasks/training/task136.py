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


def generate(rows=None, cols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of two vertical coordinates where pixels should be placed
    cols: a list of two horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    while True:
      rows = common.randint(1, 8), common.randint(0, 7)
      cols = common.randint(1, 8), common.randint(0, 7)
      # Boxes can't be overlapping, and diagonals must be at least 3 cells apart
      if abs(rows[0] - rows[1]) < 3 and abs(cols[0] - cols[1]) < 3: continue
      if abs((rows[0] - cols[0]) - (rows[1] - cols[1])) < 3: continue
      break

  grid, output = common.grids(size, size)
  for color in range(2):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      r, c = rows[color] + dr, cols[color] + dc
      output[r][c] = grid[r][c] = color + 1
  r, c = rows[0], cols[0]
  while r >= 0 and c >= 0:
    output[r][c] = 1
    r, c = r - 1, c - 1
  r, c = rows[1], cols[1]
  while r < size and c < size:
    output[r][c] = 2
    r, c = r + 1, c + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 6], cols=[2, 4]),
      generate(rows=[7, 0], cols=[6, 2]),
      generate(rows=[5, 2], cols=[3, 5]),
  ]
  test = [
      generate(rows=[3, 5], cols=[6, 2]),
  ]
  return {"train": train, "test": test}
