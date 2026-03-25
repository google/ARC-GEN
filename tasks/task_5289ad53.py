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


def generate(width=None, height=None, rows=None, cols=None, lengths=None,
             colors=None, bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the lines.
    cols: The columns of the lines.
    lengths: The lengths of the lines.
    colors: The colors of the lines.
    bgcolor: The background color of the grid.
  """

  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    while True:
      num_green, num_red = common.randint(1, 4), common.randint(1, 4)
      if num_green + num_red <= 6: break
    num_lines = num_green + num_red
    while True:
      lengths = [common.randint(2, width // 2) for _ in range(num_lines)]
      talls = [1] * num_lines
      rows = [common.randint(1, height - 2) for _ in range(num_lines)]
      cols = [common.randint(0, width - length) for length in lengths]
      if not common.overlaps(rows, cols, lengths, talls, 1): break
    colors = [3] * num_green + [2] * num_red
    bgcolor = common.choice([0, 1, 4, 5, 6, 7, 8, 9])

  grid, output = common.grid(width, height, bgcolor), common.grid(3, 2)
  for row, col, length, color in zip(rows, cols, lengths, colors):
    for c in range(col, col + length):
      grid[row][c] = color
  greens, reds = colors.count(3), colors.count(2)
  index = 0
  for _ in range(greens):
    output[index // 3][index % 3] = 3
    index += 1
  for _ in range(reds):
    output[index // 3][index % 3] = 2
    index += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=10, rows=[1, 3, 5, 7, 8], cols=[2, 9, 0, 8, 1], lengths=[4, 3, 3, 4, 5], colors=[3, 2, 3, 3, 2], bgcolor=1),
      generate(width=10, height=10, rows=[1, 3, 4, 7], cols=[0, 1, 6, 4], lengths=[4, 2, 3, 4], colors=[3, 2, 2, 3], bgcolor=5),
      generate(width=15, height=13, rows=[2, 4, 6, 8, 10, 11], cols=[2, 7, 2, 9, 1, 8], lengths=[4, 5, 6, 5, 3, 4], colors=[2, 3, 3, 2, 2, 2], bgcolor=8),
      generate(width=19, height=10, rows=[1, 1, 3, 5, 6], cols=[0, 12, 2, 14, 5], lengths=[6, 4, 8, 4, 3], colors=[3, 2, 3, 3, 3], bgcolor=8),
  ]
  test = [
      generate(width=10, height=15, rows=[1, 3, 7, 9, 11, 13], cols=[1, 2, 5, 5, 1, 4], lengths=[4, 6, 4, 2, 2, 4], colors=[3, 2, 3, 2, 3, 2], bgcolor=0),
  ]
  return {"train": train, "test": test}
