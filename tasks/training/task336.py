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


def generate(depth=None, gap=None, gravity=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    depth: how deep the container is
    gap: how much space to put between the container and the wall
    gravity: which side of the grid the container adheres to (0: top, ...)
    size: the width and height of the (square) grid
  """
  if depth is None:
    depth = common.randint(5, 6)
    gap = common.randint(0, size - depth - 2)
    gravity = common.randint(0, 3)

  grid, output = common.grids(size, size)
  for c in range(2, size - 2):
    output[gap][c] = grid[gap][c] = common.gray()
    if c != 5:
      output[gap + depth - 1][c] = grid[gap + depth - 1][c] = common.gray()
  for r in range(gap, gap + depth):
    grid[r][size - 3] = grid[r][2] = common.gray()
    output[r][size - 3] = output[r][2] = common.gray()
  for r in range(gap + 1, gap + depth - 1):
    for c in range(3, size - 3):
      output[r][c] = common.cyan()
  for r in range(gap + depth - 1, size):
    output[r][5] = common.cyan()
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(depth=6, gap=2, gravity=0),
      generate(depth=5, gap=0, gravity=2),
  ]
  test = [
      generate(depth=5, gap=2, gravity=1),
  ]
  return {"train": train, "test": test}
