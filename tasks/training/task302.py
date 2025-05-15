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


def generate(rows=None, cols=None, lengths=None, size=12):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    lengths: a list of *total* lengths (not the creme fillings)
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols, lengths = [], [], []
    for length in [5, 4, 3]:
      r = common.randint(0, size - length)
      c = common.randint(0, size - length)
      if common.overlaps(rows + [r], cols + [c], lengths + [length],
                         lengths + [length], 1): continue
      rows.append(r)
      cols.append(c)
      lengths.append(length)

  grid, output = common.grids(size, size)
  for r, c, length in zip(rows, cols, lengths):
    for dr in range(length):
      for dc in range(length):
        output[r + dr][c + dc] = grid[r + dr][c + dc] = common.gray()
    for dr in range(length - 2):
      for dc in range(length - 2):
        grid[r + dr + 1][c + dc + 1] = common.black()
        output[r + dr + 1][c + dc + 1] = common.gray() + length - 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 6, 2], cols=[7, 6, 2], lengths=[5, 4, 3]),
      generate(rows=[4, 0, 7], cols=[6, 1, 1], lengths=[5, 4, 3]),
      generate(rows=[1, 7], cols=[1, 4], lengths=[5, 4]),
  ]
  test = [
      generate(rows=[1, 8, 4], cols=[1, 4, 8], lengths=[5, 4, 3]),
  ]
  return {"train": train, "test": test}
