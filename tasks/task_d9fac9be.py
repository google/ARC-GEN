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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             center=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    center: the color of the center cell
  """
  if rows is None:
    width, height = common.randint(5, 12), common.randint(5, 12)
    color_list = common.random_colors(2)
    bitmap = common.grid(width, height)
    for pixel in common.random_pixels(width, height, 0.2):
      bitmap[pixel[0]][pixel[1]] = common.choice(color_list)
    row, col = common.randint(2, height - 3), common.randint(2, width - 3)
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        bitmap[row + dr][col + dc] = color_list[1]
    center = bitmap[row][col] = color_list[0]
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid, output = common.grid(width, height), common.grid(1, 1, center)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=5,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4],
               cols=[0, 5, 8, 1, 2, 3, 1, 2, 3, 6, 1, 2, 3, 7, 0, 5],
               colors=[2, 2, 2, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 2, 2, 2],
               center=2),
      generate(width=9, height=7,
               rows=[0, 0, 0, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 6,
                     6],
               cols=[0, 2, 8, 4, 2, 5, 6, 7, 0, 3, 5, 6, 7, 5, 6, 7, 2, 0, 3,
                     7],
               colors=[8, 8, 8, 8, 8, 3, 3, 3, 8, 3, 3, 8, 3, 3, 3, 3, 8, 3, 8,
                       8],
               center=8),
      generate(width=9, height=11,
               rows=[0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 6, 6, 6, 7, 7, 7,
                     7, 7, 8, 8, 8, 8, 9, 10],
               cols=[0, 1, 5, 2, 0, 2, 3, 5, 7, 8, 1, 4, 8, 6, 1, 2, 3, 0, 1, 2,
                     3, 7, 1, 2, 3, 8, 2, 3],
               colors=[1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2,
                       1, 2, 2, 2, 2, 2, 2, 1, 2],
               center=1),
      generate(width=12, height=11,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 7,
                     7, 7, 8, 8, 8, 8, 9, 9, 9, 10],
               cols=[1, 10, 11, 0, 7, 9, 1, 2, 3, 11, 3, 4, 0, 10, 3, 4, 1, 3,
                     4, 5, 8, 10, 2, 3, 4, 5, 3, 4, 5, 2],
               colors=[8, 3, 8, 3, 8, 3, 3, 3, 8, 8, 3, 8, 3, 8, 3, 8, 3, 3, 3,
                       3, 8, 3, 3, 3, 8, 3, 3, 3, 3, 3],
               center=8),
  ]
  test = [
      generate(width=12, height=12,
               rows=[0, 1, 1, 1, 3, 3, 3, 4, 4, 5, 5, 5, 5, 6, 7, 7, 8, 8, 8, 8,
                     9, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11],
               cols=[9, 0, 6, 9, 4, 5, 8, 1, 3, 5, 7, 8, 11, 0, 3, 8, 4, 5, 6,
                     11, 0, 4, 5, 6, 7, 4, 5, 6, 11, 2, 3, 7],
               colors=[1, 1, 4, 1, 1, 4, 4, 4, 1, 1, 4, 4, 1, 1, 1, 4, 1, 1, 1,
                       4, 4, 1, 4, 1, 1, 1, 1, 1, 4, 4, 4, 1],
               center=4),
  ]
  return {"train": train, "test": test}
