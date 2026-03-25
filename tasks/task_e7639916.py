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


def generate(width=None, height=None, rows=None, cols=None, flip=None,
             flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    flip: Whether to flip the output grid.
    flop: Whether to flop the output grid.
  """

  if width is None:
    width, height = common.randint(8, 20), common.randint(8, 20)
    wide, tall = common.randint(5, width - 2), common.randint(5, height - 2)
    r = common.randint(1, height - tall - 1)
    c = common.randint(1, width - wide - 1)
    rows = [r, r + common.randint(1, tall - 2), r + tall - 1]
    cols = [c, c + wide - 1, c + common.randint(1, wide - 2)]
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for row in range(rows[0], rows[2] + 1):
    output[row][cols[0]] = output[row][cols[1]] = 1
  for col in range(cols[0], cols[1] + 1):
    output[rows[0]][col] = output[rows[2]][col] = 1
  for row, col in zip(rows, cols):
    output[row][col] = grid[row][col] = 8
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=8, rows=[1, 4, 6], cols=[2, 9, 3],
               flip=True, flop=False),
      generate(width=20, height=10, rows=[1, 2, 8], cols=[3, 16, 10],
               flip=False, flop=False),
      generate(width=13, height=11, rows=[1, 4, 9], cols=[2, 10, 4],
               flip=True, flop=True),
  ]
  test = [
      generate(width=13, height=14, rows=[3, 5, 12], cols=[3, 11, 8],
               flip=False, flop=False),
  ]
  return {"train": train, "test": test}
