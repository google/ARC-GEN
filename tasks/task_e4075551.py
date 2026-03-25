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


def generate(width=None, height=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  if width is None:
    width, height = common.randint(14, 16), common.randint(14, 16)
    wide, tall = common.randint(7, 11), common.randint(7, 11)
    row = common.randint(1, height - tall - 1)
    col = common.randint(1, width - wide - 1)
    rows = [row,
            row + common.randint(3, tall - 4),
            row + common.randint(3, tall - 4),
            row + common.randint(3, tall - 4),
            row + tall - 1]
    cols = [col + common.randint(3, wide - 4),
            col,
            col + common.randint(3, wide - 4),
            col + wide - 1,
            col + common.randint(3, wide - 4)]
    colors = common.random_colors(5, exclude=[2, 5])
    colors[2] = 2

  grid, output = common.grids(width, height)
  # Draw the grey lines
  for row in range(rows[0], rows[4] + 1):
    output[row][cols[2]] = 5
  for col in range(cols[1], cols[3] + 1):
    output[rows[2]][col] = 5
  # Draw the other lines
  for row in range(rows[0], rows[4] + 1):
    output[row][cols[1]] = colors[1]
    output[row][cols[3]] = colors[3]
  for col in range(cols[1], cols[3] + 1):
    output[rows[0]][col] = colors[0]
    output[rows[4]][col] = colors[4]
  # Draw the pixels
  for row, col, color in zip(rows, cols, colors):
    output[row][col] = grid[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=15, rows=[2, 8, 8, 5, 12],
               cols=[6, 3, 7, 10, 6], colors=[4, 8, 2, 7, 6]),
      generate(width=15, height=14, rows=[1, 4, 7, 5, 11],
               cols=[5, 2, 5, 9, 3], colors=[8, 4, 2, 3, 6]),
      generate(width=15, height=15, rows=[3, 9, 6, 7, 13],
               cols=[4, 2, 6, 12, 5], colors=[3, 1, 2, 6, 9]),
  ]
  test = [
      generate(width=15, height=16, rows=[1, 9, 7, 7, 13],
               cols=[7, 2, 4, 11, 6], colors=[1, 7, 2, 3, 4]),
  ]
  return {"train": train, "test": test}
