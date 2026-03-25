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


def generate(width=None, height=None, rows=None, cols=None, offset=None,
             redline=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: the offset of the green creature
    redline: the horizontal coordinate of the redline
    flip: whether to flip the input grid horizontally
    xpose: whether to transpose the input grid
  """
  if width is None:
    width, height = common.randint(16, 18), common.randint(4, 5)
    pixels = common.continuous_creature(common.randint(8, 9), height, height)
    rows, cols = zip(*pixels)
    offset, redline = common.randint(0, 3), common.randint(width - 6, width - 2)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    grid[r][c + offset] = common.green()
    output[r][c + redline - max(cols) - 1] = common.green()
  for r in range(height):
    output[r][redline] = grid[r][redline] = common.red()
    output[r][redline - max(cols) - 2] = common.cyan()
  if flip: grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=4, rows=[0, 1, 1, 1, 2, 2, 3, 3, 3],
               cols=[1, 1, 2, 3, 0, 1, 1, 2, 3], offset=0, redline=10, flip=0,
               xpose=0),
      generate(width=17, height=5, rows=[4, 3, 3, 2, 1, 1, 1, 0, 0, 0],
               cols=[2, 2, 3, 3, 0, 2, 3, 0, 1, 2], offset=1, redline=15,
               flip=0, xpose=1),
      generate(width=17, height=5, rows=[0, 0, 0, 1, 1, 2, 3, 3, 3],
               cols=[0, 1, 2, 0, 2, 2, 0, 1, 2], offset=3, redline=13, flip=1,
               xpose=1),
  ]
  test = [
      generate(width=18, height=4, rows=[0, 0, 1, 1, 2, 2, 2, 3],
               cols=[0, 1, 0, 2, 0, 1, 2, 2], offset=4, redline=13, flip=1,
               xpose=0),
  ]
  return {"train": train, "test": test}
