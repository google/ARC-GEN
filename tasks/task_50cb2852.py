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
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of widths of the rectangles
    talls: a list of heights of the rectangles
    colors: a list of colors of the rectangles
  """
  if rows is None:
    width = common.randint(12, 14)
    height = width + common.randint(-2, 2)
    num_boxes = common.randint(2, 4)
    while True:
      wides = [common.randint(3, 8) for _ in range(num_boxes)]
      talls = [common.randint(3, 8) for _ in range(num_boxes)]
      rows = [common.randint(0, height - t) for t in talls]
      cols = [common.randint(0, width - w) for w in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break
    while True:
      colors = [common.randint(1, 3) for _ in range(num_boxes)]
      if len(set(colors)) > 1: break

  grid, output = common.grids(width, height)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        output[r][c] = grid[r][c] = color
        if r not in [row, row + tall - 1] and c not in [col, col + wide - 1]:
          output[r][c] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=13, rows=[1, 1, 8], cols=[2, 10, 8],
               wides=[5, 3, 7], talls=[6, 3, 5], colors=[2, 1, 3]),
      generate(width=11, height=12, rows=[1, 7], cols=[1, 2], wides=[4, 6],
               talls=[4, 3], colors=[2, 1]),
      generate(width=13, height=12, rows=[1, 2, 8], cols=[6, 0, 2],
               wides=[4, 4, 8], talls=[6, 4, 4], colors=[2, 3, 1]),
  ]
  test = [
      generate(width=13, height=14, rows=[0, 1, 5, 7], cols=[1, 8, 2, 9],
               wides=[5, 3, 6, 4], talls=[4, 3, 6, 7], colors=[1, 1, 2, 3]),
  ]
  return {"train": train, "test": test}
