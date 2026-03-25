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


def generate(width=None, height=None, size=None, brow=None, bcol=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: width of the input grid.
    height: height of the input grid.
    size: size of the box.
    brow: row of the box.
    bcol: column of the box.
    colors: colors of the corners.
  """

  if width is None:
    width, height = common.randint(11, 14), common.randint(11, 14)
    size = 2 * common.randint(3, 4) + 1
    brow = common.randint(1, height - size - 1)
    bcol = common.randint(1, width - size - 1)
    colors = common.random_colors(4, exclude=[5])
    colors[common.randint(0, 3)] = 0

  grid, output = common.grids(width, height)
  output[brow][bcol] = grid[brow][bcol] = colors[0]
  output[brow][bcol + size - 1] = grid[brow][bcol + size - 1] = colors[1]
  output[brow + size - 1][bcol] = grid[brow + size - 1][bcol] = colors[2]
  output[brow + size - 1][bcol + size - 1] = grid[brow + size - 1][bcol + size - 1] = colors[3]
  half = size // 2 - 1
  output[brow + half][bcol + half] = colors[0]
  output[brow + half][bcol + half + 2] = colors[1]
  output[brow + half + 1][bcol + half + 1] = 5
  output[brow + half + 2][bcol + half] = colors[2]
  output[brow + half + 2][bcol + half + 2] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, size=7, brow=3, bcol=2, colors=[0, 2, 8, 6]),
      generate(width=12, height=10, size=7, brow=1, bcol=3, colors=[2, 1, 3, 0]),
  ]
  test = [
      generate(width=14, height=12, size=9, brow=2, bcol=3, colors=[3, 8, 9, 0]),
  ]
  return {"train": train, "test": test}
