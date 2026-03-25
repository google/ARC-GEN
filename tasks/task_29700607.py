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


def generate(size=None, colors=None, offset=None, rows=None, mcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the lines.
    offset: The offset of the legend.
    rows: The rows of the lines.
    mcol: The middle column selection.
  """

  if size is None:
    size = common.randint(10, 15)
    colors = common.random_colors(3)
    offset = common.randint(3, size - 6)
    rows = common.sample(list(range(2, size - 1)), 3)
    if rows[0] == max(rows): rows[0], rows[1] = rows[1], rows[0]
    if rows[2] == max(rows): rows[2], rows[1] = rows[1], rows[2]
    mcol = common.randint(0, 2) - 1
    if mcol == 0: rows[1] = size

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    grid[0][offset + i] = color
  grid[rows[0]][0] = colors[0]
  if mcol: grid[rows[1]][0 if mcol == -1 else (size - 1)] = colors[1]
  grid[rows[2]][size - 1] = colors[2]

  # Color #0
  for row in range(0, rows[0]):
    output[row][offset] = colors[0]
  for col in range(0, offset + 1):
    output[rows[0]][col] = colors[0]

  # Color #1
  for row in range(0, rows[1]):
    output[row][offset + 1] = colors[1]
  if mcol:
    lb = (offset + 1) if mcol == 1 else 0
    ub = size if mcol == 1 else (offset + 2)
    for col in range(lb, ub):
      output[rows[1]][col] = colors[1]

  # Color #2
  for row in range(0, rows[2]):
    output[row][offset + 2] = colors[2]
  for col in range(offset + 2, size):
    output[rows[2]][col] = colors[2]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, colors=[5, 3, 8], offset=4, rows=[4, 8, 5], mcol=-1),
      generate(size=15, colors=[6, 5, 3], offset=5, rows=[4, 15, 2], mcol=0),
      generate(size=11, colors=[4, 6, 2], offset=3, rows=[4, 9, 4], mcol=1),
  ]
  test = [
      generate(size=11, colors=[4, 8, 5], offset=3, rows=[7, 11, 9], mcol=0),
  ]
  return {"train": train, "test": test}
