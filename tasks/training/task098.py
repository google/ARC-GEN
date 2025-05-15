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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    height = common.randint(8, 20)
    width = height + common.randint(-2, 2)
    num_boxes = max(1, (width + height) // 5 - 2)
    while True:
      wides = [common.randint(3, 8) for _ in range(num_boxes)]
      talls = [common.randint(3, 8) for _ in range(num_boxes)]
      if max(wides) > width - 2 or max(talls) > height - 2: continue  # Too big.
      rows = [common.randint(1, height - tall - 1) for tall in talls]
      cols = [common.randint(1, width - wide - 1) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break
    colors = common.random_colors(num_boxes)

  grid, output = common.grids(width, height)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        output[r][c] = grid[r][c] = color
    for r in range(row + 1, row + tall - 1):
      for c in range(col + 1, col + wide - 1):
        output[r][c] = common.black()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=18, rows=[1, 3, 10, 10], cols=[1, 6, 2, 12],
               wides=[4, 7, 7, 3], talls=[3, 5, 4, 5], colors=[8, 3, 6, 7]),
      generate(width=7, height=8, rows=[1], cols=[1], wides=[5], talls=[4],
               colors=[2]),
      generate(width=12, height=11, rows=[1, 6], cols=[2, 1], wides=[8, 6],
               talls=[4, 4], colors=[5, 4]),
  ]
  test = [
      generate(width=19, height=17, rows=[1, 1, 5, 6, 13],
               cols=[1, 11, 2, 10, 5], wides=[6, 4, 6, 8, 5],
               talls=[3, 3, 7, 6, 3], colors=[8, 6, 4, 1, 3]),
  ]
  return {"train": train, "test": test}
