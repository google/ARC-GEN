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


def generate(size=None, rows=None, cols=None, lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of lengths
  """
  if size is None:
    size = common.randint(5, 10)
    rows, cols, lengths = [], [], []
    r = common.randint(0, 1)
    while r < size:
      length = 2 * common.randint(1, (size // 2) - 1) + 1
      c = common.randint(0, size - length)
      rows.append(r)
      cols.append(c)
      lengths.append(length)
      rand = common.randint(0, 9)
      if rand in [0]:
        r += 1
      elif rand in [1, 2, 3]:
        r += 3
      else:
        r += 2

  grid, output = common.grids(size, size)
  for r, c, length in zip(rows, cols, lengths):
    for x in range(length):
      if x % 2 == 0:
        output[r][c + x] = grid[r][c + x] = common.blue()
      else:
        output[r][c + x] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[0, 3], cols=[0, 1], lengths=[3, 3]),
      generate(size=10, rows=[1, 4, 6, 8], cols=[1, 2, 6, 3],
               lengths=[7, 3, 3, 3]),
      generate(size=10, rows=[1, 2, 5, 7, 9], cols=[6, 1, 3, 4, 1],
               lengths=[3, 3, 5, 3, 3]),
  ]
  test = [
      generate(size=10, rows=[0, 2, 4, 5, 7], cols=[1, 2, 1, 5, 3],
               lengths=[3, 7, 3, 3, 3]),
  ]
  return {"train": train, "test": test}
