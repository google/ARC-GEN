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


def generate(width=None, height=None, length=None, first=None, second=None,
             rows=None, cols=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    length: the length of the portals
    first: the row of the first portal
    second: the column of the first portal
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flip: whether to flip the input grid
  """

  def draw(grid, output):
    num_yellow = 0
    for r in range(length):
      grid[first + r][0] = grid[second + r][width - 1] = common.red()
      output[first + r][0] = output[second + r][width - 1] = common.red()
    for r, c in zip(rows, cols):
      grid[first + r][c] = common.cyan()
      output[first + r][c] = common.yellow()
      num_yellow += 1
      for col in range(width):
        if col + 1 < width:
          output[second + r][col] = common.cyan()
        else:
          output[second + r][col] = common.red()
        if col >= c: continue
        output[first + r][col] = common.cyan() if col > 0 else common.red()
    for r in range(height):
      if grid[r][0] == common.red() and grid[r][width - 1] == common.red():
        return False
    return num_yellow > 1

  if width is None:
    while True:
      width, height = common.randint(8, 12), common.randint(16, 24)
      flip, length = common.randint(0, 1), common.randint(4, 6)
      first = common.randint(1, 4) if flip else 1
      second = height - length - (1 if flip else common.randint(1, 4))
      rows, cols = [], []
      for r in range(length):
        if common.randint(0, 1) == 0: continue
        rows.append(r)
        cols.append(common.randint(2, width - 2))
      grid, output = common.grids(width, height)
      if draw(grid, output): break

  grid, output = common.grids(width, height)
  draw(grid, output)
  if flip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=19, length=4, first=1, second=11, rows=[2],
               cols=[4], flip=0),
      generate(width=10, height=20, length=5, first=1, second=11, rows=[1, 3],
               cols=[7, 5], flip=0),
      generate(width=10, height=20, length=6, first=3, second=13,
               rows=[1, 2, 4], cols=[3, 7, 5], flip=1),
  ]
  test = [
      generate(width=12, height=21, length=6, first=1, second=14,
               rows=[1, 2, 4], cols=[8, 7, 4], flip=0),
  ]
  return {"train": train, "test": test}
