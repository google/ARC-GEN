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


def generate(rows=None, cols=None, colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    grid, rows, cols, colors = common.grid(size, size), [], [], []
    for idx, color in enumerate(common.random_colors(common.randint(6, 9))):
      pixels_remaining = common.randint(2, 7) if idx else 1
      while pixels_remaining:
        r = common.randint(0 if idx else 1, size - (1 if idx else 2))
        c = common.randint(0 if idx else 1, size - (1 if idx else 2))
        if grid[r][c]: continue
        grid[r][c] = color
        pixels_remaining -= 1
        rows.append(r)
        cols.append(c)
        colors.append(color)

  grid, output = common.grids(size, size)
  min_color = min(set(colors), key=colors.count)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    if color != min_color: continue
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        output[r + dr][c + dc] = common.red()
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 2, 2, 2, 3, 3, 4, 6, 7, 7, 7, 8, 8, 8, 8, 9],
               cols=[3, 7, 0, 5, 9, 2, 9, 2, 1, 1, 2, 4, 1, 2, 6, 8, 7],
               colors=[1, 5, 2, 2, 1, 1, 5, 8, 4, 5, 1, 1, 8, 1, 1, 3, 3]),
      generate(rows=[0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 4, 5, 5, 6, 6, 6, 6,
                     7, 7, 7, 7, 8, 8, 9, 9],
               cols=[0, 1, 2, 3, 5, 9, 3, 8, 9, 3, 7, 9, 7, 0, 4, 8, 1, 3, 4, 8,
                     0, 1, 5, 9, 7, 8, 4, 5],
               colors=[2, 7, 7, 1, 3, 3, 9, 3, 7, 1, 6, 9, 1, 9, 2, 3, 5, 7, 3,
                       1, 4, 4, 1, 5, 5, 3, 4, 5]),
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 6, 6, 8, 9],
               cols=[0, 4, 8, 9, 1, 4, 6, 8, 1, 3, 1, 9, 5, 1, 3, 6, 2],
               colors=[6, 8, 2, 8, 7, 2, 5, 2, 9, 1, 9, 1, 6, 1, 7, 3, 5]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 6, 6,
                     7, 7, 7, 7, 7, 7, 8, 8, 9, 9, 9, 9],
               cols=[4, 5, 6, 3, 4, 6, 6, 2, 4, 9, 0, 1, 2, 3, 4, 9, 3, 6, 5, 7,
                     0, 1, 3, 6, 7, 9, 2, 9, 0, 2, 8, 9],
               colors=[2, 5, 7, 5, 6, 2, 3, 8, 3, 8, 7, 4, 7, 7, 4, 4, 8, 7, 9,
                       4, 5, 5, 3, 6, 7, 7, 3, 2, 1, 1, 6, 7]),
  ]
  return {"train": train, "test": test}
