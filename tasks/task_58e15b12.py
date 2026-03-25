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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, colors=[3, 8]):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
  """

  if width is None:
    width, height = common.randint(15, 20), common.randint(20, 25)
    wides = [common.randint(3, 6) for _ in range(2)]
    talls = [common.randint(1, 5) for _ in range(2)]
    while True:
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      bcols = [common.randint(1, width - wide - 1) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 2): break

  grid, output = common.grids(width, height)
  for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
    # Draw the bottom half.
    left, rite = bcol, bcol + wide - 1
    for row in range(brow, height, tall):
      for r in range(tall):
        if row == brow: grid[row + r][left] = grid[row + r][rite] = color
        hue = color if common.get_pixel(output, row + r, left) == 0 else 6
        common.draw(output, row + r, left, hue)
        hue = color if common.get_pixel(output, row + r, rite) == 0 else 6
        common.draw(output, row + r, rite, hue)
      left, rite = left - 1, rite + 1
    # Draw the upper half.
    left, rite = bcol - 1, bcol + wide
    for row in range(brow - 1, -tall, -tall):
      for r in range(tall):
        hue = color if common.get_pixel(output, row - r, left) == 0 else 6
        common.draw(output, row - r, left, hue)
        hue = color if common.get_pixel(output, row - r, rite) == 0 else 6
        common.draw(output, row - r, rite, hue)
      left, rite = left - 1, rite + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=22, wides=[3, 4], talls=[3, 2], brows=[1, 7], bcols=[12, 3]),
      generate(width=17, height=23, wides=[4, 3], talls=[3, 4], brows=[17, 6], bcols=[10, 3]),
      generate(width=19, height=24, wides=[5, 3], talls=[4, 1], brows=[6, 19], bcols=[4, 11]),
  ]
  test = [
      generate(width=20, height=24, wides=[6, 4], talls=[3, 5], brows=[3, 10], bcols=[11, 5]),
  ]
  return {"train": train, "test": test}
