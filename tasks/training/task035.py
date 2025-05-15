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
             size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the pool
    height: the height of the pool
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if width is None:
    width, height = common.randint(2, 4), common.randint(2, 5)
    rows, cols, colors = [], [], []
    for r in range(3, 3 + height):
      for c in range(6 - width, 6):
        coords = []
        if r == 3:
          coords.append((0, c))
        if r == 2 + height:
          coords.append((size - 1, c))
        if c == 6 - width:
          coords.append((r, 0))
        if c == 5:
          coords.append((r, size - 1))
        if not coords or common.randint(0, 1) == 0: continue
        coord = common.choice(coords)
        rows.append(coord[0])
        cols.append(coord[1])
        colors.append(common.random_color(exclude=[common.cyan()]))

  grid, output = common.grids(size, size)
  for r in range(3, 3 + height):
    for c in range(6 - width, 6):
      output[r][c] = grid[r][c] = common.cyan()
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = grid[r][c] = color
    r = r if r >= 3 else 3
    r = r if r <= 2 + height else 2 + height
    c = c if c >= 6 - width else 6 - width
    c = c if c <= 5 else 5
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=4, rows=[0, 6, 9], cols=[4, 0, 5],
               colors=[9, 6, 4]),
      generate(width=3, height=5, rows=[0, 3, 5, 7, 9], cols=[4, 0, 9, 0, 5],
               colors=[7, 6, 2, 3, 1]),
      generate(width=3, height=5, rows=[0, 3, 4, 6, 7, 9],
               cols=[3, 9, 0, 0, 9, 3], colors=[4, 6, 3, 2, 2, 7]),
  ]
  test = [
      generate(width=4, height=4, rows=[0, 0, 3, 4, 5, 6, 9],
               cols=[3, 5, 0, 9, 0, 0, 4], colors=[6, 2, 9, 7, 3, 4, 6]),
  ]
  return {"train": train, "test": test}
