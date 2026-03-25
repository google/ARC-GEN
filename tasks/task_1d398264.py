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


def generate(size=None, colors=None, brow=None, bcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
    brow: The row of the box.
    bcol: The column of the box.
  """

  if size is None:
    size = common.randint(10, 20)
    center = common.random_color()
    colors = [common.random_color(exclude=[center]) for _ in range(size * size)]
    colors[4] = center
    brow, bcol = common.randint(1, size - 4), common.randint(1, size - 4)

  grid, output = common.grids(size, size)
  for row in [-1, 0, 1]:
    for col in [-1, 0, 1]:
      r, c = brow + row + 1, bcol + col + 1
      color = colors[(row + 1) * 3 + col + 1]
      output[r][c] = grid[r][c] = color
      if row == 0 and col == 0: continue
      while r >= 0 and c >= 0 and r < size and c < size:
        output[r][c] = color
        r, c = r + row, c + col
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, colors=[6, 2, 2, 4, 5, 4, 6, 8, 8], brow=6, bcol=15),
      generate(size=10, colors=[3, 1, 2, 2, 6, 2, 2, 7, 7], brow=2, bcol=3),
      generate(size=15, colors=[2, 5, 7, 2, 8, 7, 3, 3, 3], brow=1, bcol=2),
  ]
  test = [
      generate(size=16, colors=[4, 2, 5, 2, 9, 5, 4, 1, 1], brow=2, bcol=3),
      generate(size=12, colors=[6, 1, 1, 6, 7, 1, 3, 3, 1], brow=2, bcol=3),
  ]
  return {"train": train, "test": test}
