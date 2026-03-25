# Copyright 2026 Google LLC
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


def generate(width=None, height=None, rows=None, lengths=None, pcol=None,
             flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the segments.
    lengths: The lengths of the segments.
    pcol: The column of the red pixel.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 15)
    pcol = common.randint(3, width - 4)
    row, rows, lengths = 0, [], []
    while True:
      row += common.randint(2, 3)
      if row + 2 >= height: break
      num_segments = common.randint(2, 4)
      while True:
        the_lengths = [common.randint(1, width) for _ in range(num_segments)]
        if sum(the_lengths) + num_segments - 1 == width: break
      rows.extend([row] * num_segments)
      lengths.extend(the_lengths)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for row in set(rows):
    col = 0
    for length, r in zip(lengths, rows):
      if r != row: continue
      for c in range(length):
        output[row][col + c] = grid[row][col + c] = 8
      col += length + 1
  grid[0][pcol] = 2
  queue = [(0, pcol)]
  while queue:
    row, col = queue.pop()
    if output[row][col] == 2: continue  # Already visited.
    output[row][col] = 2
    if row + 1 >= height: continue
    if output[row + 1][col] == 0: queue.append((row + 1, col))
    if output[row + 1][col] == 8:
      if col - 1 >= 0: queue.append((row, col - 1))
      if col + 1 < width: queue.append((row, col + 1))
  if flip: grid, output = common.flip(grid), common.flip(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, rows=[2, 2, 2, 5, 5, 9, 9, 9],
               lengths=[5, 2, 2, 3, 7, 6, 1, 2], pcol=3, flip=False,
               xpose=True),
      generate(width=17, height=11, rows=[2, 2, 2, 4, 4, 4, 7, 7],
               lengths=[5, 3, 7, 2, 9, 4, 5, 11], pcol=7, flip=False,
               xpose=False),
      generate(width=10, height=13, rows=[3, 3, 3, 7, 7, 10, 10, 10, 10],
               lengths=[2, 2, 4, 8, 1, 1, 1, 4, 1], pcol=4, flip=True,
               xpose=True),
  ]
  test = [
      generate(width=14, height=15,
               rows=[2, 2, 4, 4, 4, 4, 7, 7, 7, 10, 10, 10, 10],
               lengths=[4, 9, 2, 4, 3, 2, 2, 6, 4, 4, 2, 3, 2], pcol=6,
               flip=False, xpose=False),
  ]
  return {"train": train, "test": test}
