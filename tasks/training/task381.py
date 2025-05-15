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


def generate(rows=None, cols=None, wides=None, talls=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          output[r][c] = grid[r][c] = common.red()
    for r in range(size):
      last_red, danger = size, False  # "Danger": we'd touch a box above / below
      for c in range(size):
        if output[r][c] != common.red():
          danger = danger or common.get_pixel(output, r - 1, c) == common.red()
          danger = danger or common.get_pixel(output, r + 1, c) == common.red()
          continue
        for col in range(last_red + 1, c):
          output[r][col] = common.maroon() if not danger else common.black()
        last_red, danger = c, False
    # Avoid maroons in top or bottom row.
    if common.maroon() in output[0] or common.maroon() in output[-1]:
      return False
    # For all other rows, many sure there's no open space between red's.
    for r in range(1, size - 1):
      state = 0
      for color in output[r]:
        if state == 0 and color == common.red(): state = 1
        if state == 1 and color == common.black(): state = 2
        if state == 2 and color == common.red(): return False
    return True

  if rows is None:
    num_boxes = common.randint(3, 5)
    while True:
      wides = [common.randint(1, 4) for _ in range(num_boxes)]
      talls = [common.randint(2, 6) for _ in range(num_boxes)]
      rows = [common.randint(0, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      grid, output = common.grids(size, size)
      if not draw(grid, output): continue
      if not common.overlaps(rows, cols, wides, talls, 1): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 3, 6], cols=[0, 7, 3], wides=[3, 2, 2],
               talls=[3, 5, 4]),
      generate(rows=[0, 2, 5, 8], cols=[0, 7, 3, 6], wides=[2, 3, 2, 4],
               talls=[4, 4, 4, 2]),
      generate(rows=[0, 1, 3, 6, 7], cols=[6, 0, 5, 9, 0],
               wides=[4, 4, 3, 1, 4], talls=[2, 3, 6, 4, 3]),
  ]
  test = [
      generate(rows=[0, 1, 3, 5], cols=[0, 6, 1, 5], wides=[3, 4, 3, 4],
               talls=[2, 3, 5, 2]),
  ]
  return {"train": train, "test": test}
