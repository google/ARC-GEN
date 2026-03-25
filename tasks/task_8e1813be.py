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


def generate(
    width=None,
    height=None,
    offset=None,
    row=None,
    col=None,
    xpose=None,
    colors=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    offset: the offset of the stripes
    row: the row of the gray square
    col: the column of the gray square
    xpose: whether to transpose the grids
    colors: a list of colors for the stripes
  """
  if width is None:
    height = common.randint(9, 21)
    width = height + common.randint(0, 3)
    offset = common.randint(0, 2)
    num_stripes = (height + 2 - offset) // 3
    colors = common.sample([1, 2, 3, 4, 6, 7, 8, 9], num_stripes)
    row, col, box_placement = 0, 0, common.randint(0, 2)
    if box_placement == 1: row = common.randint(0, height - len(colors) - 2)
    if box_placement == 2: col = common.randint(0, width - len(colors) - 2)
    xpose = common.randint(0, 1)

  grid = common.grid(width, height)
  output = common.grid(len(colors), len(colors))
  # Draw the input stripes.
  for idx, r in enumerate(range(offset, height, 3)):
    for c in range(width):
      grid[r][c] = colors[idx]
  # Draw the black border.
  for r in range(len(colors) + 2):
    for c in range(len(colors) + 2):
      grid[row + r][col + c] = common.black()
  # Draw the gray square.
  for r in range(len(colors)):
    for c in range(len(colors)):
      grid[row + r + 1][col + c + 1] = common.gray()
  # Draw the output stripes.
  for r in range(len(colors)):
    for c in range(len(colors)):
      output[r][c] = colors[r]
  # Flips the grids if needed.
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=18, offset=2, row=9, col=0, xpose=0,
               colors=[2, 1, 3, 4, 8, 6]),
      generate(width=12, height=10, offset=2, row=0, col=0, xpose=1,
               colors=[1, 2, 4]),
      generate(width=12, height=12, offset=1, row=0, col=5, xpose=0,
               colors=[2, 8, 4, 1]),
  ]
  test = [
      generate(width=19, height=19, offset=0, row=0, col=7, xpose=0,
               colors=[2, 3, 8, 4, 6, 1, 7]),
  ]
  return {"train": train, "test": test}
