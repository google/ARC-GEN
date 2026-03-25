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


def generate(rows=None, cols=None, size=9, b=0, u=1, g=5):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
    b: the integer used for all background cells
    u: the integer used for all "blue" cells
    g: the integer used for all "gray" cells
  """
  if rows is None:
    num_boxes = common.randint(3, 4)
    while True:
      rows = [common.randint(1, size - 2) for _ in range(num_boxes)]
      cols = [common.randint(1, size - 2) for _ in range(num_boxes)]
      lengths = [3] * num_boxes
      if not common.overlaps(rows, cols, lengths, lengths): break

  grid, output = common.grids(size, size, b)
  for r, c in zip(rows, cols):
    grid[r][c] = g
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      output[r + dr][c + dc] = u
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
      output[r + dr][c + dc] = g
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 5, 7], cols=[3, 6, 2]),
      generate(rows=[1, 1, 5, 7], cols=[2, 7, 2, 6]),
  ]
  test = [
      generate(rows=[1, 3, 5, 7], cols=[1, 4, 7, 2]),
  ]
  return {"train": train, "test": test}
