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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    wides: The wides of the boxes.
    talls: The talls of the boxes.
    colors: The colors of the boxes.
  """

  if width is None:
    while True:
      num_colors, height = common.randint(2, 6), common.randint(6, 8)
      colors = common.random_colors(num_colors, exclude=[8])
      col = 2 * num_colors + 1 + common.randint(0, 1)
      rows, cols, wides, talls = [], [], [], []
      for _ in range(num_colors):
        while True:
          wide, tall = common.randint(2, 4), common.randint(2, 5)
          row = common.randint(0, height - tall)
          if rows and rows[-1] == row: continue
          if talls and talls[-1] == tall: continue
          if rows and talls and rows[-1] + talls[-1] == row + tall: continue
          break
        wides.append(wide)
        talls.append(tall)
        cols.append(col)
        rows.append(row)
        col += wide + common.randint(0, 1)
      width = col
      if width <= 30: break

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    for r in range(height):
      grid[r][2 * i + 1] = color
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    common.rect(grid, wide, tall, row, col, 8)
    common.rect(output, wide, tall, row, col, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=6, rows=[0, 2, 0], cols=[7, 10, 12],
               wides=[3, 2, 3], talls=[2, 4, 3], colors=[1, 6, 7]),
      generate(width=20, height=8, rows=[1, 3, 1], cols=[8, 12, 15],
               wides=[4, 2, 4], talls=[4, 4, 4], colors=[4, 3, 2]),
      generate(width=18, height=7, rows=[0, 1, 0, 3], cols=[9, 11, 14, 16],
               wides=[2, 2, 2, 2], talls=[2, 3, 5, 3], colors=[3, 2, 4, 7]),
  ]
  test = [
      generate(width=28, height=7, rows=[0, 3, 1, 0, 2, 1],
               cols=[13, 16, 18, 20, 23, 26], wides=[3, 2, 2, 3, 3, 2],
               talls=[3, 4, 3, 2, 5, 4], colors=[1, 3, 2, 4, 6, 7]),
  ]
  return {"train": train, "test": test}
