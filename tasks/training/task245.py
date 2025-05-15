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


def generate(width=None, height=None, roff=None, coff=None, brow=None,
             bcol=None, rows=None, cols=None, size=7):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    roff: a vertical offset for the red sprite
    coff: a horizontal offset for the red sprite
    brow: a vertical coordinate where the green box should be placed
    bcol: a horizontal coordinate where the green box should be placed
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if width is None:
    width, height = common.randint(7, 10), common.randint(7, 10)
    brow = common.randint(0, height - size)
    bcol = common.randint(0, width - size)
    rows, cols = common.conway_sprite(size - 2, size - 2, size * 2)
    if common.randint(0, 1):  # TODO: Also allow a diagonal shift.
      roff, coff = 0, 0 - common.randint(1, bcol + 1)
    else:
      roff, coff = 0 - common.randint(1, brow + 1), 0

  grid, output = common.grids(width, height)
  for r, c in [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]:
    output[brow + r][bcol + c] = grid[brow + r][bcol + c] = common.green()
  for row, col in zip(rows, cols):
    r, c = brow + row + 1, bcol + col + 1
    output[r][c] = grid[roff + r][coff + c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7, roff=-1, coff=-1, brow=0, bcol=0,
               rows=[0, 1, 1, 2, 2, 2, 2, 2, 3, 4, 4],
               cols=[2, 1, 2, 0, 1, 2, 3, 4, 1, 1, 2]),
      generate(width=9, height=9, roff=0, coff=-2, brow=1, bcol=1,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4],
               cols=[2, 3, 4, 0, 1, 2, 0, 2, 0, 1, 2, 3, 3]),
      generate(width=10, height=9, roff=-2, coff=0, brow=1, bcol=1,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4],
               cols=[1, 2, 0, 1, 2, 3, 2, 3, 4, 2, 1, 2]),
      generate(width=8, height=9, roff=0, coff=-1, brow=0, bcol=0,
               rows=[0, 1, 1, 1, 2, 3, 3, 3, 3, 3, 4],
               cols=[3, 1, 2, 3, 1, 0, 1, 2, 3, 4, 1]),
  ]
  test = [
      generate(width=8, height=10, roff=0, coff=-1, brow=1, bcol=0,
               rows=[0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4],
               cols=[0, 0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 0]),
  ]
  return {"train": train, "test": test}
