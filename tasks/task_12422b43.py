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


def generate(width=None, height=None, depth=None, length=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    depth: The depth of the given pattern.
    length: The length of the pattern to be copied.
    colors: A list of colors to use.
  """

  if width is None:
    width, height = common.randint(5, 7), common.randint(5, 15)
    depth = common.randint(2, height // 2 + 1)
    length = common.randint(1, depth - 1)
    center = common.randint(2, width - 2)
    grid = common.grid(width, depth)
    for r in range(depth):
      left = center + common.randint(-1, 0)
      right = center + common.randint(0, 1)
      color = common.random_color(exclude=[5])
      for c in range(left, right + 1):
        grid[r][c] = color
      c = common.randint(0, width - 1)
      if grid[r][c]: grid[r][c] = common.random_color(exclude=[5])
    colors = common.flatten(grid)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = grid[i // width][i % width] = color
  for r in range(depth, height):
    for c in range(width):
      output[r][c] = grid[(r - depth) % length][c]
  for r in range(length):
    output[r][0] = grid[r][0] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=13, depth=5, length=4,
               colors=[0, 0, 0, 3, 3, 0,
                       0, 0, 0, 3, 2, 0,
                       0, 0, 0, 2, 3, 0,
                       0, 0, 0, 8, 8, 0,
                       0, 0, 0, 8, 8, 0]),
      generate(width=7, height=8, depth=5, length=3,
               colors=[0, 0, 8, 8, 0, 0, 0,
                       0, 0, 0, 7, 0, 0, 0,
                       0, 0, 0, 4, 4, 0, 0,
                       0, 0, 3, 3, 0, 0, 0,
                       0, 0, 1, 1, 0, 0, 0]),
      generate(width=7, height=9, depth=5, length=2,
               colors=[0, 0, 0, 4, 4, 0, 0,
                       0, 0, 8, 8, 8, 0, 0,
                       0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 3, 3, 0, 0,
                       0, 0, 4, 4, 0, 0, 0]),
      generate(width=6, height=7, depth=2, length=1,
               colors=[0, 0, 6, 8, 0, 0,
                       0, 0, 8, 3, 0, 0]),
      generate(width=5, height=5, depth=3, length=2,
               colors=[0, 0, 6, 0, 0,
                       0, 4, 4, 4, 0,
                       0, 0, 6, 0, 0]),
  ]
  test = [
      generate(width=7, height=10, depth=4, length=3,
               colors=[0, 0, 4, 4, 4, 0, 0,
                       0, 0, 0, 8, 0, 0, 0,
                       0, 0, 0, 6, 0, 0, 0,
                       0, 0, 2, 2, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
