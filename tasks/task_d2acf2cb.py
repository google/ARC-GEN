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


def generate(width=None, height=None, cdir=None, switch=None, vals=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    cdir: The direction of the lines.
    switch: Whether to switch the input / output.
    vals: The values of the lines.
    colors: The colors to use.
  """

  if width is None:
    width, height = common.randint(6, 10), common.randint(6, 10)
    cdir, switch = common.randint(0, 1), common.randint(0, 1)
    val, vals = -1, []
    while True:
      val += common.randint(2, 4)
      if val + 1 >= (width if cdir else height): break
      vals.append(val)
    colors = [0 if common.randint(0, 1) else 6 for _ in range(width * height)]

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = grid[i // width][i % width] = color
  thegrid = grid if switch else output
  for val in vals:
    if cdir:
      output[0][val] = grid[0][val] = 4
      output[height - 1][val] = grid[height - 1][val] = 4
      for r in range(1, height - 1):
        thegrid[r][val] = 7 if thegrid[r][val] else 8
    else:
      output[val][0] = grid[val][0] = 4
      output[val][width - 1] = grid[val][width - 1] = 4
      for c in range(1, width - 1):
        thegrid[val][c] = 7 if thegrid[val][c] else 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=9, cdir=0, switch=True, vals=[1, 4, 7],
               colors=[0, 6, 0, 6, 6, 0, 6, 0, 6,
                       0, 6, 0, 6, 0, 0, 0, 0, 0,
                       0, 6, 6, 6, 6, 6, 6, 6, 0,
                       0, 0, 6, 0, 6, 6, 0, 0, 6,
                       0, 0, 6, 6, 6, 6, 0, 0, 0,
                       0, 0, 0, 0, 6, 0, 0, 0, 6,
                       6, 0, 6, 0, 6, 0, 0, 6, 0,
                       0, 6, 0, 0, 6, 0, 6, 6, 0,
                       6, 6, 0, 6, 0, 6, 6, 0, 0]),
      generate(width=9, height=7, cdir=0, switch=False, vals=[5],
               colors=[0, 6, 0, 0, 0, 6, 6, 0, 0,
                       6, 6, 6, 6, 6, 6, 6, 6, 6,
                       0, 6, 6, 6, 6, 0, 0, 0, 0,
                       6, 6, 0, 0, 0, 6, 6, 0, 0,
                       0, 6, 6, 6, 0, 0, 6, 0, 6,
                       0, 0, 0, 6, 6, 6, 6, 0, 0,
                       0, 6, 6, 6, 0, 6, 6, 0, 0]),
      generate(width=9, height=6, cdir=1, switch=False, vals=[3, 7],
               colors=[6, 0, 6, 0, 6, 0, 0, 0, 6,
                       6, 0, 6, 0, 0, 6, 0, 0, 6,
                       0, 6, 6, 0, 0, 0, 0, 6, 0,
                       6, 6, 6, 0, 0, 0, 0, 6, 6,
                       6, 0, 0, 6, 6, 0, 0, 0, 6,
                       6, 6, 6, 0, 0, 6, 6, 0, 0]),
  ]
  test = [
      generate(width=9, height=10, cdir=1, switch=False, vals=[1, 5, 7],
               colors=[0, 0, 6, 6, 0, 0, 6, 0, 0,
                       0, 6, 0, 0, 0, 6, 6, 6, 0,
                       0, 0, 0, 6, 0, 0, 6, 6, 6,
                       6, 6, 6, 0, 0, 0, 6, 0, 0,
                       0, 6, 0, 6, 0, 0, 6, 0, 0,
                       0, 6, 6, 0, 6, 6, 0, 6, 6,
                       6, 6, 6, 6, 0, 6, 0, 6, 6,
                       0, 6, 0, 6, 6, 6, 6, 6, 6,
                       6, 0, 0, 0, 6, 0, 0, 6, 0,
                       0, 0, 0, 0, 6, 0, 6, 0, 0]),
  ]
  return {"train": train, "test": test}
