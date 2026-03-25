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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    colors: The colors of the grid.
  """

  if width is None:
    width, height = common.randint(2, 10), common.randint(1, 10)
    subset = common.random_colors(4)
    grid = common.grid(width, height)
    while 0 in common.flatten(grid):
      angle, color = common.randint(0, 3), common.choice(subset)
      if angle == 0:  # Horiz
        row, length = common.randint(0, height - 1), common.randint(1, width)
        col = common.randint(0, width - length)
        for c in range(length): grid[row][col + c] = color
      if angle == 1:  # Vertical
        col, length = common.randint(0, width - 1), common.randint(1, height)
        row = common.randint(0, height - length)
        for r in range(length): grid[row + r][col] = color
      if angle == 2:  # Slash
        val = common.randint(-width - height, width + height)
        for r in range(height):
          for c in range(width):
            if r - c == val: grid[r][c] = color
      if angle == 3:  # Backslash
        val = common.randint(-width - height, width + height)
        for r in range(height):
          for c in range(width):
            if r + c == val: grid[r][c] = color
    colors = common.flatten(grid)

  grid, output = common.grid(width, height), common.grid(width + height - 1, height)
  for r in range(height):
    for c in range(width):
      output[r][c + height - 1 - r] = grid[r][c] = colors[r * width + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=4, colors=[9, 7, 9, 7, 7, 7, 5, 5, 5,
                                          4, 7, 9, 7, 9, 7, 7, 5, 5,
                                          4, 4, 7, 7, 9, 7, 9, 7, 5,
                                          4, 4, 4, 7, 7, 7, 9, 7, 9]),
      generate(width=6, height=6, colors=[4, 8, 8, 8, 8, 7,
                                          1, 4, 8, 8, 7, 8,
                                          4, 1, 4, 7, 8, 8,
                                          6, 4, 1, 4, 8, 8,
                                          6, 6, 4, 1, 4, 8,
                                          6, 6, 6, 4, 1, 4]),
      generate(width=4, height=7, colors=[1, 6, 6, 6,
                                          1, 6, 6, 6,
                                          1, 6, 6, 6,
                                          1, 8, 8, 8,
                                          1, 5, 5, 5,
                                          1, 5, 5, 5,
                                          1, 5, 5, 5]),
  ]
  test = [
      generate(width=1, height=4, colors=[1, 9, 5, 4]),
      generate(width=2, height=10, colors=[1, 1,
                                           1, 1,
                                           6, 8,
                                           6, 8,
                                           6, 8,
                                           6, 8,
                                           4, 4,
                                           4, 4,
                                           5, 5,
                                           5, 5]),
      generate(width=4, height=2, colors=[5, 4, 9, 8, 8, 5, 2, 9]),
  ]
  return {"train": train, "test": test}
