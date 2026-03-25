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


def generate(width=None, height=None, wide=None, tall=None, length=None,
             brow=None, bcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    width, height = common.randint(15, 30), common.randint(15, 30)
    length = common.randint(1, 4)
    wide, tall = (width - 2 * length) // 4 - 1, (height - 2 * length) // 4 - 1
    wide, tall = wide * 4 + 3 + 2 * length, tall * 4 + 3 + 2 * length
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    colors = common.random_colors(3, exclude=[1])
    extra = common.random_color(exclude=colors + [1]) if common.randint(0, 1) else 0
    colors = [extra] + colors

  grid, output = common.grids(width, height, colors[0])
  # Draw the input blue squares.
  common.rect(grid, length, length, brow + 1, bcol + 1, 1)
  common.rect(grid, length, length, brow + tall - 1 - length, bcol + wide - 1 - length, 1)
  # Draw the output blue squares.
  common.rect(output, length, length, brow + 1, bcol + 1, 1)
  common.rect(output, length, length, brow + 1, bcol + wide - 1 - length, 1)
  common.rect(output, length, length, brow + tall - 1 - length, bcol + 1, 1)
  common.rect(output, length, length, brow + tall - 1 - length, bcol + wide - 1 - length, 1)
  # Draw the input unicolor lines.
  for i in range(length):
    grid[brow + 1 + i][bcol + length + 3] = colors[1]
    grid[brow + length + 3][bcol + 1 + i] = colors[1]
  # Draw the output unicolor lines.
  for col in range(bcol + length + 3, bcol + wide - length - 2, 4):
    for i in range(length):
      output[brow + 1 + i][col] = colors[1]
      output[brow + tall - 2 - i][col] = colors[1]
  for row in range(brow + length + 3, brow + tall - length - 2, 4):
    for i in range(length):
      output[row][bcol + 1 + i] = colors[1]
      output[row][bcol + wide - 2 - i] = colors[1]
  # Draw the input top and side.
  for i in range(length):
    grid[brow + 1 + i][bcol + length + 1] = colors[2]
    grid[brow + length + 1][bcol + 1 + i] = colors[3]
  # Draw the output top and bottom and sides.
  for col in range(bcol + length + 1, bcol + wide - length - 1):
    output[brow + tall - 1][col] = output[brow][col] = colors[2]
  for row in range(brow + length + 1, brow + tall - length - 1):
    output[row][bcol + wide - 1] = output[row][bcol] = colors[3]
  for col in range(bcol + length + 1, bcol + wide - length, 4):
    for i in range(length):
      output[brow + tall - 2 - i][col] = output[brow + 1 + i][col] = colors[2]
  for row in range(brow + length + 1, bcol + tall - length, 4):
    for i in range(length):
      output[row][bcol + wide - 2 - i] = output[row][bcol + 1 + i] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=26, height=24, wide=21, tall=21, length=3, brow=1, bcol=2,
               colors=[0, 2, 4, 8]),
      generate(width=22, height=18, wide=19, tall=15, length=2, brow=1, bcol=0,
               colors=[4, 8, 2, 3]),
  ]
  test = [
      generate(width=16, height=19, wide=13, tall=17, length=1, brow=1, bcol=1,
               colors=[0, 8, 2, 4]),
      generate(width=30, height=30, wide=27, tall=27, length=4, brow=0, bcol=1,
               colors=[8, 6, 3, 4]),
  ]
  return {"train": train, "test": test}
