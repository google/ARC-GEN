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


def generate(prow=None, pcol=None, brow=None, bcol=None, length=None,
             color=None, notch=None, size=10, pink=6, orange=7):
  """Returns input and output grids according to the given parameters.

  Args:
    prow: The row of the pink box.
    pcol: The column of the pink box.
    brow: The row of the mini box.
    bcol: The column of the mini box.
    length: The length of the pink box.
    color: The color of the mini box.
    notch: The placement of the notch.
    size: The size of the grid.
    pink: The color of the pink box.
    orange: The color of the orange box.
  """

  if prow is None:
    length = common.randint(3, 8)
    color = common.random_color(exclude=[pink, orange])
    while True:
      prow, pcol = common.randint(0, size - length), common.randint(0, size - length)
      brow, bcol = common.randint(0, size - 2), common.randint(0, size - 2)
      rows, cols = [brow, prow], [bcol, pcol]
      if not common.overlaps(rows, cols, [length, 2], [length, 2]): break
    notch = -1 if length == 3 else common.randint(-1, 3)

  grid, output = common.grids(size, size, orange)
  common.hollow_rect(grid, length, length, prow, pcol, pink)
  common.hollow_rect(output, length, length, prow, pcol, pink)
  mini_size = 1 if length == 3 else 2
  common.rect(grid, mini_size, mini_size, brow, bcol, color)
  common.rect(output, length - 2, length - 2, prow + 1, pcol + 1, color)
  if notch != -1:
    grid[brow + notch // 2][bcol + notch % 2] = orange
    row, col = prow + 1 + notch // 2, pcol + 1 + notch % 2
    common.rect(output, length - 3, length - 3, row, col, orange)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prow=1, pcol=1, brow=7, bcol=1, length=5, color=5, notch=-1),
      generate(prow=1, pcol=1, brow=8, bcol=8, length=3, color=2, notch=-1),
      generate(prow=3, pcol=1, brow=0, bcol=1, length=6, color=8, notch=1),
  ]
  test = [
      generate(prow=2, pcol=0, brow=0, bcol=8, length=8, color=9, notch=2),
  ]
  return {"train": train, "test": test}
