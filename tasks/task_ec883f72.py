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


def generate(size=None, width=None, height=None, row=None, col=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    width: the width of antenna man
    height: the height of antenna man
    row: the row of antenna man
    col: the column of antenna man
    colors: a list of digits representing the colors to be used
  """

  def draw(grid, output):
    # Draw the outer ring.
    for r in range(row - 2, row + height + 2):
      for c in range(col - 2, col + width + 2):
        common.draw(grid, r, c, colors[1])
        common.draw(output, r, c, colors[1])
    # Draw the middle ring.
    for r in range(row - 1, row + height + 1):
      for c in range(col - 1, col + width + 1):
        common.draw(grid, r, c, common.black())
        common.draw(output, r, c, common.black())
    # Draw the inner ring.
    for r in range(row, row + height):
      for c in range(col, col + width):
        common.draw(grid, r, c, colors[0])
        common.draw(output, r, c, colors[0])
    # Draw the antenna.
    for i in range(size):
      common.draw(output, row - 3 - i, col - 3 - i, colors[0])
      common.draw(output, row - 3 - i, col + width + 2 + i, colors[0])
      common.draw(output, row + height + 2 + i, col - 3 - i, colors[0])
      common.draw(output, row + height + 2 + i, col + width + 2 + i, colors[0])
    return grid != output

  if size is None:
    while True:
      size = common.randint(6, 12)
      width, height = common.randint(2, 5), common.randint(2, 5)
      row = common.randint(0, size - 1)
      col = common.randint(0, size - 1)
      colors = common.random_colors(2)
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=6, width=2, height=2, row=0, col=0, colors=[3, 9]),
      generate(size=8, width=1, height=1, row=0, col=4, colors=[6, 8]),
      generate(size=9, width=2, height=2, row=7, col=3, colors=[2, 4]),
      generate(size=12, width=4, height=5, row=7, col=0, colors=[4, 5]),
  ]
  test = [
      generate(size=12, width=2, height=3, row=0, col=6, colors=[4, 3]),
  ]
  return {"train": train, "test": test}
