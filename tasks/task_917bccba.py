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


def generate(size=None, brow=None, bcol=None, row=None, col=None, bcolor=None,
             color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the box.
    brow: The row of the box.
    bcol: The column of the box.
    row: The row of the cross.
    col: The column of the cross.
    bcolor: The color of the box.
    color: The color of the cross.
  """

  if size is None:
    size = common.randint(5, 8)
    brow, bcol = common.randint(1, 11 - size), common.randint(1, 11 - size)
    row = brow + common.randint(2, size - 3)
    col = bcol + common.randint(2, size - 3)
    colors = common.random_colors(2)
    bcolor, color = colors[0], colors[1]

  grid, output = common.grids(12, 12)
  for i in range(12):
    grid[row][i] = grid[i][col] = color
    output[brow][i] = output[i][bcol + size - 1] = color
  common.hollow_rect(grid, size, size, brow, bcol, bcolor)
  common.hollow_rect(output, size, size, brow, bcol, bcolor)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, brow=3, bcol=2, row=6, col=5, bcolor=1, color=8),
      generate(size=6, brow=2, bcol=2, row=5, col=4, bcolor=2, color=3),
      generate(size=5, brow=3, bcol=4, row=5, col=6, bcolor=3, color=4),
  ]
  test = [
      generate(size=8, brow=2, bcol=2, row=5, col=6, bcolor=7, color=6),
  ]
  return {"train": train, "test": test}
