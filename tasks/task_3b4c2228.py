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


def generate(width=None, height=None, rows=None, cols=None, sizes=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    sizes: The sizes of the boxes.
    colors: The colors of the boxes.
  """

  def draw():
    if len(set(sizes)) == 1: return None, None  # Need one of each size.
    blues = 0
    grid, output = common.grid(width, height), common.grid(3, 3)
    for row, col, size, color in zip(rows, cols, sizes, colors):
      common.rect(grid, size, size, row, col, color)
      if size == 2 and color == 3: blues += 1
    if blues < 1 or blues > 3: return None, None
    for i in range(blues):
      output[i][i] = 1
    return grid, output

  if width is None:
    width, height = common.randint(5, 8), common.randint(5, 8)
    area = width * height
    while True:
      red_boxes = common.randint(area // 16, area // 8)
      green_boxes = common.randint(area // 16, area // 8)
      red_sizes = [common.randint(1, 2) for _ in range(red_boxes)]
      green_sizes = [common.randint(1, 2) for _ in range(green_boxes)]
      red_rows = [common.randint(0, height - size) for size in red_sizes]
      red_cols = [common.randint(0, width - size) for size in red_sizes]
      green_rows = [common.randint(0, height - size) for size in green_sizes]
      green_cols = [common.randint(0, width - size) for size in green_sizes]
      if common.overlaps(green_rows, green_cols, green_sizes, green_sizes):
        continue
      if common.some_abutted(green_rows, green_cols, green_sizes, green_sizes):
        continue
      if common.overlaps(red_rows, red_cols, red_sizes, red_sizes):
        continue
      if common.some_abutted(red_rows, red_cols, red_sizes, red_sizes):
        continue
      rows = red_rows + green_rows
      cols = red_cols + green_cols
      sizes = red_sizes + green_sizes
      if common.overlaps(rows, cols, sizes, sizes): continue
      colors = [2] * len(red_sizes) + [3] * len(green_sizes)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=7, rows=[0, 3, 3, 5], cols=[1, 0, 4, 3],
               sizes=[2, 2, 1, 2], colors=[3, 2, 2, 2]),
      generate(width=7, height=5, rows=[0, 0, 2, 3, 3, 4],
               cols=[1, 6, 4, 0, 4, 2], sizes=[2, 1, 1, 1, 2, 1],
               colors=[3, 3, 2, 3, 3, 3]),
      generate(width=5, height=5, rows=[0, 1, 3, 4], cols=[3, 0, 2, 0],
               sizes=[2, 2, 2, 1], colors=[2, 3, 2, 3]),
      generate(width=7, height=7, rows=[0, 1, 1, 3, 3, 5],
               cols=[2, 0, 5, 0, 4, 2], sizes=[2, 1, 1, 2, 2, 2],
               colors=[3, 2, 3, 3, 2, 3]),
      generate(width=7, height=7, rows=[0, 0, 0, 1, 3, 3, 3, 5, 6, 6],
               cols=[0, 3, 6, 3, 0, 1, 5, 4, 0, 2],
               sizes=[2, 1, 1, 2, 1, 2, 2, 2, 1, 1],
               colors=[2, 3, 3, 2, 2, 3, 2, 3, 3, 2]),
  ]
  test = [
      generate(width=8, height=8, rows=[0, 1, 1, 2, 2, 3, 4, 4, 6, 7, 7],
               cols=[1, 5, 6, 0, 7, 2, 0, 5, 1, 4, 6],
               sizes=[2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1],
               colors=[3, 3, 2, 2, 3, 2, 3, 3, 3, 2, 3]),
      generate(width=5, height=8, rows=[1, 3, 4, 5, 6], cols=[1, 0, 4, 0, 3],
               sizes=[2, 1, 1, 2, 2], colors=[3, 2, 3, 3, 2]),
  ]
  return {"train": train, "test": test}
