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


def generate(lengths=None, talls=None, rows=None, cols=None, flip=None,
             size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: the lengths of the two rectangles
    talls: the tallness of the two rectangles
    rows: the rows where the rectangles are placed
    cols: the columns where the rectangles are placed
    flip: whether to flip the grid vertically
    size: the width and height of the (square) grid
  """
  if lengths is None:
    while True:
      border = common.randint(3, 5)
      lengths = [common.randint(3, 7) for _ in range(2)]
      talls = [common.randint(max(3, border - 1), border),
               common.randint(max(3, size - border - 2), size - border - 1)]
      if lengths[0] != lengths[1] and talls[0] != talls[1]: continue  # no match
      if lengths[0] == lengths[1] and talls[0] == talls[1]: continue  # same!
      if lengths[0] > lengths[1] or talls[0] > talls[1]: continue  # red smaller
      break
    rows = [border - talls[0], border + 1]
    cols = [common.randint(0, size - length) for length in lengths]
    flip = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for idx in range(2):
    length, tall, row, col = lengths[idx], talls[idx], rows[idx], cols[idx]
    for r in range(row, row + tall):
      for c in range(col, col + length):
        output[r][c] = grid[r][c] = common.yellow()
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + length - 1):
        output[r][c] = idx + 1
  if flip:
    grid, output = grid[::-1], output[::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[4, 6], talls=[4, 4], rows=[1, 6], cols=[1, 3], flip=0),
      generate(lengths=[4, 5], talls=[3, 5], rows=[0, 4], cols=[5, 1], flip=1),
  ]
  test = [
      generate(lengths=[6, 6], talls=[3, 6], rows=[0, 4], cols=[4, 0], flip=1),
  ]
  return {"train": train, "test": test}
