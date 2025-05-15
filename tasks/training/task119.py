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


def generate(depth=None, mid=None, shown=None, flip=None, gravity=None,
             size=12):
  """Returns input and output grids according to the given parameters.

  Args:
    depth: how many cells deep the wall is
    mid: the horizontal placement of the rebounding point
    shown: how many cells in the diagonal are shown
    flip: whether we should flip the grid so the diagonal starts from the right
    gravity: which side of the grid the wall adheres to (0: top, 1: left, ...)
    size: the width and height of the (square) grid
  """
  if depth is None:
    depth = common.randint(1, size // 2 - 1)
    mid = common.randint(depth, size - depth - 2)
    shown = common.randint(2, 3)
    flip = common.randint(0, 1)
    gravity = common.randint(0, 3)

  grid = common.grid(size, size)
  for r in range(size):
    for c in range(size):
      grid[r][c] = common.red() if r < depth else common.black()
  for c in range(size):
    r = depth + (mid - c if c < mid else c - mid)
    grid[r][c] = common.green() if c >= shown else common.cyan()
  grid = grid if not flip else [row[::-1] for row in grid]
  grid = common.apply_gravity(grid, gravity)
  output = [row[:] for row in grid]
  for r in range(size):
    for c in range(size):
      if grid[r][c] == common.green(): grid[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(depth=2, mid=7, shown=2, flip=1, gravity=3),
      generate(depth=3, mid=6, shown=3, flip=0, gravity=2),
      generate(depth=2, mid=6, shown=3, flip=1, gravity=1),
  ]
  test = [
      generate(depth=4, mid=4, shown=2, flip=0, gravity=3),
  ]
  return {"train": train, "test": test}
