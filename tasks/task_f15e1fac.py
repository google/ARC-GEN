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


def generate(width=None, height=None, rows=None, cols=None, flip=None,
             gravity=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flip: whether to flip the grid
    gravity: which direction the gravity is pulling
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    rows, cols = [], []
    row = 0
    # Create the red dots along the side
    while True:
      row += common.randint(4, 7)
      if row + 1 >= height: break
      rows.append(row)
    col = -1
    # Create the sky blue dots along the top
    while True:
      col += common.randint(2, 4)
      if col >= width: break
      cols.append(col)
    flip, gravity = common.randint(0, 1), common.randint(0, 3)

  grid, output = common.grids(width, height)
  for r in rows:
    output[r][0] = grid[r][0] = common.red()
  for c in cols:
    output[0][c] = grid[0][c] = common.cyan()
  inc = 0
  for r in range(1, height):
    inc += 1 if r in rows else 0
    for c in cols:
      if c + inc >= width: continue
      output[r][c + inc] = common.cyan()
  if flip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=17, rows=[4, 10], cols=[1, 5, 7, 9], flip=0,
               gravity=0),
      generate(width=10, height=14, rows=[3, 7, 11], cols=[3, 7], flip=1,
               gravity=0),
      generate(width=12, height=12, rows=[4, 8], cols=[2, 5, 9], flip=1,
               gravity=1),
  ]
  test = [
      generate(width=12, height=17, rows=[5, 10, 14], cols=[1, 3, 6, 9], flip=1,
               gravity=3),
  ]
  return {"train": train, "test": test}
