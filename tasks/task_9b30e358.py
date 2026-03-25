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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    width, bgcolor = common.randint(5, 7), common.random_color()
    subset = common.random_colors(2, exclude=[bgcolor])
    wide, line = common.randint(3, width), common.randint(4, 5)
    bcol, symm = common.randint(0, width - wide), common.randint(0, 1)
    grid = common.grid(width, 10, bgcolor)
    for r in range(line):
      for c in common.sample(list(range(wide)), common.randint(1, wide)):
        color = common.choice(subset)
        grid[9 - r][bcol + c] = color
        if symm: grid[9 - r][bcol + wide - 1 - c] = color
    colors = common.flatten(grid)

  width, height, bgcolor, line = len(colors) // 10, 10, colors[0], None
  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = grid[i // width][i % width] = color
    if line is None and color != bgcolor: line = height - i // width
  for row in range(height):
    r = (height - 1 - row) % line
    r = height - 1 - r
    for col in range(width):
      output[row][col] = grid[r][col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5,
                       5, 2, 2, 2, 5,
                       5, 5, 2, 5, 5,
                       5, 8, 8, 5, 5,
                       5, 5, 8, 8, 5,
                       5, 5, 8, 5, 5]),
      generate(colors=[3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 3, 3, 3, 3,
                       3, 3, 3, 9, 2, 9, 3,
                       3, 3, 3, 2, 9, 2, 3,
                       3, 3, 3, 9, 9, 9, 3,
                       3, 3, 3, 3, 9, 3, 3]),
  ]
  test = [
      generate(colors=[7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7,
                       7, 6, 7, 6, 7,
                       6, 7, 2, 7, 6,
                       7, 2, 6, 2, 7,
                       7, 6, 7, 6, 7]),
  ]
  return {"train": train, "test": test}
