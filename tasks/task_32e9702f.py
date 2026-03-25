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


def generate(size=None, rows=None, cols=None, widths=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the lines.
    width: The widths of the lines.
    color: The color of the lines.
  """

  if size is None:
    size = common.randint(3, 10)
    rows, color = [], common.random_color(exclude=[5])
    row = common.randint(0, 1)
    while row < size:
      rows.append(row)
      row += common.randint(2, 4)
    widths = common.sample(range(2, size), len(rows))
    cols = [common.randint(0, size - width) for width in widths]

  grid = common.grid(size, size)
  output = common.grid(size, size, 5)
  for row, col, width in zip(rows, cols, widths):
    for c in range(width):
      common.draw(grid, row, col + c, color)
      common.draw(output, row, col + c - 1, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, rows=[1, 4], cols=[2, 1], widths=[4, 2], color=3),
      generate(size=3, rows=[0], cols=[0], widths=[3], color=4),
      generate(size=7, rows=[0, 2, 4], cols=[0, 2, 1], widths=[4, 3, 5], color=7),
  ]
  test = [
      generate(size=10, rows=[0, 2, 4, 7], cols=[2, 6, 1, 4],
               widths=[5, 2, 3, 6], color=6),
  ]
  return {"train": train, "test": test}
