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


def generate(lcol=None, rows=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lcol: The column of the vertical line.
    rows: The rows of the horizontal lines.
    colors: The colors of the horizontal lines.
  """

  if lcol is None:
    lcol = common.randint(1, 14)
    num_lines = common.randint(2, 4)
    while True:
      rows = sorted(common.sample(list(range(1, 14)), num_lines))
      good = True
      for i in range(1, len(rows)):
        if rows[i] - rows[i - 1] < 3: good = False
      if good: break
    colors = common.choices([0, 2, 3, 4, 5, 6, 9], num_lines)

  grid, output = common.grid(16, 16, 7), common.grid(16, 16, 1)
  for i, (row, color) in enumerate(zip(rows, colors)):
    offset = 0 if i == 0 or colors[i] == colors[i - 1] else 2
    lb = 0 if not i else (row + rows[i - 1] + offset) // 2
    ub = 16 if i == len(rows) - 1 else (row + rows[i + 1] + 1) // 2
    common.rect(output, 16, ub - lb, lb, 0, color)
  for r in range(16):
    grid[r][lcol] = 8
    output[r][lcol] = 1
  for row, color in zip(rows, colors):
    for c in range(16):
      grid[row][c] = color if c != lcol else 1
      output[row][c] = 1 if c != lcol else 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lcol=4, rows=[2, 10, 14], colors=[9, 6, 3]),
      generate(lcol=3, rows=[4, 13], colors=[5, 2]),
      generate(lcol=8, rows=[2, 6, 13], colors=[4, 4, 0]),
  ]
  test = [
      generate(lcol=4, rows=[2, 5, 9, 13], colors=[9, 6, 6, 5]),
  ]
  return {"train": train, "test": test}
