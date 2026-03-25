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


def generate(colors=None, flip=None, flop=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: colors of the pixels.
    flip: whether to flip the grid.
    flop: whether to flop the grid.
    xpose: whether to transpose the grid.
  """

  if colors is None:
    colors = [0] * (6 * 7)
    fgcolors = common.random_colors(2, exclude=[1, 8])
    for group in [0, 1]:
      for r in range(3):
        cols = common.sample([0, 1, 2], common.randint(1, 3))
        for col in cols:
          colors[(group * 4 + r) * 6 + col] = fgcolors[group]
    for r in range(7):
      cols = common.sample([0, 1, 2], common.randint(1, 3))
      for col in cols:
        colors[r * 6 + col + 3] = 8
    flip = common.randint(0, 1)
    flop = common.randint(0, 1)
    xpose = common.randint(0, 1)
    pass

  grid, output = common.grid(30, 30), common.grid(6, 7)
  for c in range(30):
    grid[0][c] = 1
  for i, color in enumerate(colors):
    row, col = i // 6, i % 6
    output[row][col] = color
    if col > 2: col += 1
    for r, c in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
      grid[4 * row + r + 3][4 * col + c + 2 + (1 if flop else 0)] = color
  for r in range(7):
    target = 5
    for c in range(5, -1, -1):
      if output[r][c] != 0:
        temp = output[r][c]
        output[r][c] = 0
        output[r][target] = temp
        target -= 1
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 2, 2, 8, 8, 8,
                       0, 2, 0, 8, 0, 0,
                       2, 2, 2, 8, 8, 0,
                       0, 0, 0, 0, 8, 8,
                       3, 3, 3, 8, 8, 8,
                       0, 3, 3, 8, 0, 0,
                       0, 3, 3, 8, 8, 8],
               flip=False, flop=False, xpose=False),
      generate(colors=[4, 4, 4, 8, 8, 8,
                       4, 0, 4, 0, 8, 8,
                       4, 4, 4, 8, 8, 8,
                       0, 0, 0, 0, 8, 0,
                       6, 6, 0, 8, 8, 8,
                       6, 0, 6, 0, 8, 8,
                       6, 6, 0, 8, 8, 8],
               flip=True, flop=False, xpose=True),
      generate(colors=[4, 4, 4, 0, 8, 8,
                       0, 4, 4, 0, 0, 8,
                       4, 4, 0, 8, 8, 8,
                       0, 0, 0, 8, 0, 8,
                       0, 9, 0, 8, 0, 8,
                       9, 9, 9, 8, 8, 8,
                       9, 0, 9, 0, 0, 8],
               flip=True, flop=True, xpose=False),
  ]
  test = [
      generate(colors=[2, 2, 2, 8, 8, 8,
                       0, 0, 2, 0, 8, 0,
                       2, 2, 2, 0, 8, 8,
                       0, 0, 0, 0, 0, 8,
                       7, 0, 7, 0, 8, 0,
                       7, 7, 7, 8, 8, 8,
                       7, 0, 0, 0, 8, 8],
               flip=False, flop=True, xpose=True),
  ]
  return {"train": train, "test": test}
