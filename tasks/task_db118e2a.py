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


def generate(width=None, height=None, color=None, brow=None, bcol=None,
             pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    color: The color of the hollow rectangles.
    brow: The row of the pattern.
    bcol: The column of the pattern.
    pattern: The pattern of the input grid.
  """

  if width is None:
    width, height = common.randint(5, 10), common.randint(5, 10)
    brow = common.randint(0, height - 5)
    bcol = common.randint(0, width - 5)
    color = common.random_color(exclude=[7])
    subset = common.random_colors(common.randint(1, 2), exclude=[7])
    pattern = [7, 7, 7, 7, 7, 7, 7, 7, 7]
    if not common.randint(0, 4):  # Just a pixel
      pattern[4] = subset[0]
    else:
      rows, cols = common.conway_sprite()
      for row, col in zip(rows, cols):
        pattern[row * 3 + col] = common.choice(subset)

  grid, output = common.grid(width, height, 7), common.grid(15, 15, 7)
  common.hollow_rect(grid, width, height, 0, 0, color)
  common.hollow_rect(output, 5, 5, 2, 2, color)
  common.hollow_rect(output, 5, 5, 8, 8, color)
  output[2][2] = output[2][6] = output[6][2] = output[6][6] = 7
  output[8][8] = output[8][12] = output[12][8] = output[12][12] = 7
  grid[0][0] = grid[0][width - 1] = 7
  grid[height - 1][0] = grid[height - 1][width - 1] = 7
  for i, color in enumerate(pattern):
    grid[brow + 1 + i // 3][bcol + 1 + i % 3] = color
    output[3 + i // 3][3 + i % 3] = color
    output[9 + i // 3][9 + i % 3] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=9, color=4, brow=4, bcol=2,
               pattern=[9, 7, 7, 7, 7, 7, 7, 7, 1]),
      generate(width=8, height=7, color=3, brow=1, bcol=2,
               pattern=[7, 7, 7, 7, 3, 7, 7, 7, 7]),
      generate(width=9, height=9, color=9, brow=1, bcol=1,
               pattern=[7, 9, 7, 9, 7, 9, 7, 9, 7]),
      generate(width=7, height=6, color=6, brow=0, bcol=1,
               pattern=[7, 8, 7, 2, 7, 2, 2, 8, 2]),
  ]
  test = [
      generate(width=5, height=6, color=8, brow=1, bcol=0,
               pattern=[8, 8, 8, 8, 4, 7, 8, 7, 4]),
  ]
  return {"train": train, "test": test}
