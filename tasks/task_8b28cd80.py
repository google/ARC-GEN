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


def generate(row=None, col=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: The row of the pixel.
    col: The column of the pixel.
    color: The color of the pixel.
  """

  if row is None:
    row, col = common.randint(0, 2), common.randint(0, 2)
    color = common.random_color()

  grid, output = common.grid(3, 3), common.grid(9, 9)
  grid[row][col] = color
  row, col = row * 4, col * 4
  rdirs, cdirs, length = [-1, 0, 1, 0], [0, 1, 0, -1], 2
  for i in range(20):
    for _ in range(length):
      common.draw(output, row, col, color)
      row += rdirs[i % 4]
      col += cdirs[i % 4]
    if i % 4 in [1, 3]: length += 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=1, col=0, color=5),
      generate(row=1, col=2, color=8),
      generate(row=0, col=2, color=7),
      generate(row=0, col=1, color=3),
      generate(row=1, col=1, color=4),
  ]
  test = [
      generate(row=2, col=0, color=3),
      generate(row=2, col=2, color=6),
  ]
  return {"train": train, "test": test}
