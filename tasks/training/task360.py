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


def generate(rows=None, cols=None, colors=None, lefts=None, rights=None,
             width=4, height=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digit representing the colors to be used
    lefts: a list of 0/1 values if we belong on the left
    rights: a list of 0/1 values if we belong on the right
    width: the width of the grid
    height: the height of the grid
  """
  if rows is None:
    rows, cols, colors, lefts, rights = [], [], [], [], []
    color_list = common.random_colors(2, exclude=[common.gray()])
    for r in range(common.randint(1, 2), height - common.randint(1, 2)):
      idx = 0
      for c in range(common.randint(1, 4)):
        idx = idx if common.randint(0, 1) else 1
        side = common.randint(0, 2)
        rows.append(r)
        cols.append(c)
        colors.append(color_list[idx])
        lefts.append(1 if side < 2 else 0)
        rights.append(1 if side > 0 else 0)

  grid = common.grid(2 * width + 1, height)
  output = common.grid(width, height)
  for r in range(height):
    grid[r][width] = common.gray()
  for r, c, color, left, right in zip(rows, cols, colors, lefts, rights):
    grid[r][width - c - 1] = color if left else common.black()
    grid[r][width + c + 1] = color if right else common.black()
    output[r][width - c - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 3, 3, 4, 4, 5, 6, 6, 6, 7],
               cols=[0, 0, 1, 0, 1, 0, 0, 1, 2, 0],
               colors=[4, 4, 4, 3, 3, 3, 3, 3, 3, 3],
               lefts=[1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
               rights=[0, 1, 1, 0, 0, 0, 1, 1, 1, 0]),
      generate(rows=[1, 2, 2, 3, 4, 4, 4, 5, 5, 6, 7, 7, 7, 8],
               cols=[0, 0, 1, 0, 0, 1, 2, 0, 1, 0, 0, 1, 2, 0],
               colors=[2, 2, 6, 2, 2, 2, 2, 6, 6, 2, 2, 2, 2, 2],
               lefts=[1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
               rights=[0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0]),
      generate(rows=[1, 2, 3, 4, 4, 4, 5, 5, 6, 7, 8, 8],
               cols=[0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 1],
               colors=[7, 8, 8, 8, 8, 7, 8, 8, 8, 8, 8, 7],
               lefts=[0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
               rights=[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1]),
  ]
  test = [
      generate(rows=[1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 7, 7, 8],
               cols=[0, 0, 0, 1, 2, 3, 0, 1, 0, 1, 2, 0, 0, 1, 0],
               colors=[1, 1, 1, 1, 1, 6, 6, 6, 1, 1, 1, 1, 1, 6, 6],
               lefts=[1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
               rights=[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
