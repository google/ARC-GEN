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


def generate(width=None, height=None, col=None, offset=None, flip=None,
             xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    col: The column of the cyan.
    offset: The numeric offset.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    grid, output = common.grids(width, height)
    for r in range(height):
      for c in range(width):
        grid[r][c] = 1 if (r + c) % 2 == offset else 0
    for c in range(width):
      num_blue = sum(grid[r][c] for r in range(height))
      for r in range(num_blue):
        output[height - 1 - r][c] = 1
      if c == col:
        for r in range((height - 1) // 2):
          output[height - 1 - num_blue - r][c] = 9
    if grid[height - 1][col] != 1: return None, None
    output[height - 1][col] = grid[height - 1][col] = 8
    if flip: grid, output = common.flip(grid), common.flip(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if width is None:
    width, height = common.randint(3, 9), common.randint(3, 9)
    offset = common.randint(0, 1)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)
    while True:
      col = common.randint(1, width - 2)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=6, col=1, offset=0, flip=False, xpose=True),
      generate(width=7, height=7, col=4, offset=0, flip=True, xpose=True),
      generate(width=8, height=4, col=2, offset=1, flip=False, xpose=False),
      generate(width=3, height=3, col=1, offset=1, flip=True, xpose=False),
  ]
  test = [
      generate(width=5, height=5, col=2, offset=0, flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
