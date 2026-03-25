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


def generate(width=None, height=None, length=None, spacing=None, col=None,
             color=None, offset=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    length: The length of the red boxes.
    spacing: The spacing between the red boxes.
    col: The column where the leftmost green line lies.
    color: The color of the input bofder.
    offset: The row where the red boxes start.
    xpose: Whether to transpose the grids.
  """

  if width is None:
    width, height = common.randint(15, 19), common.randint(18, 19)
    length = common.randint(1, 4)
    spacing = common.randint(2, 3)
    col = common.randint(4, 6)
    color = common.random_color(exclude=[2, 3])
    offset = common.randint(1, 2)
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height)
  # Draw the thick output lines.
  for row in range(offset, height, length + spacing):
    for r in range(row, row + length):
      for c in range(width):
        common.draw(output, r, c, color)
  # Draw the green stripes.
  for row in range(height):
    output[row][col] = grid[row][col] = 3
    output[row][col + length + 1] = grid[row][col + length + 1] = 3
  # Draw the red boxes.
  for row in range(offset, height, length + spacing):
    for r in range(row, row + length):
      for c in range(col + 1, col + 1 + length):
        common.draw(grid, r, c, 2)
        common.draw(output, r, c, 2)
  common.hollow_rect(grid, width, height, 0, 0, color)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=18, length=3, spacing=3, col=6, color=8,
               offset=1, xpose=False),
      generate(width=14, height=18, length=2, spacing=2, col=4, color=4,
               offset=1, xpose=True),
      generate(width=15, height=19, length=1, spacing=2, col=4, color=6,
               offset=2, xpose=False),
  ]
  test = [
      generate(width=19, height=19, length=4, spacing=2, col=6, color=1,
               offset=1, xpose=True),
  ]
  return {"train": train, "test": test}
