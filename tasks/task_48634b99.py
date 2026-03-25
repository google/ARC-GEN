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


def generate(selected=None, top=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    selected: The selected index.
    top: Whether to shade the top of the line.
    rows: The rows of the lines.
    cols: The columns of the lines.
  """

  if selected is None:
    selected, top = common.randint(1, 4), common.randint(0, 1)
    num_lines = common.randint(10, 15)
    while True:
      rows = [common.randint(0, 16 - max(10 - 2 * idx, 2)) for idx in range(num_lines)]
      cols = [common.randint(0, 15) for _ in range(num_lines)]
      wides = [2] * num_lines
      talls = [max(10 - 2 * idx, 2) + 1 for idx in range(num_lines)]
      if not common.overlaps(rows, cols, wides, talls): break

  grid, output = common.grids(16, 16, 7)
  for idx, (row, col) in enumerate(zip(rows, cols)):
    length = max(10 - 2 * idx, 2)
    for i in range(length):
      output[row + i][col] = grid[row + i][col] = 8
      if idx == selected and (i >= length // 2) != int(top):
        grid[row + i][col] = 9
      if idx + 1 == selected and (i >= length // 2) != int(top):
        output[row + i][col] = 9
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(selected=3, top=1, rows=[0, 8, 1, 3, 7, 10, 11, 11, 13, 14],
               cols=[6, 14, 2, 9, 12, 1, 4, 12, 7, 4]),
      generate(selected=4, top=0,
               rows=[6, 4, 7, 1, 9, 0, 1, 5, 6, 6, 12, 12, 13],
               cols=[4, 9, 1, 1, 13, 15, 11, 7, 11, 14, 13, 15, 11]),
      generate(selected=1, top=0,
               rows=[0, 0, 10, 0, 1, 5, 5, 6, 8, 8, 8, 10, 12, 13, 14],
               cols=[14, 9, 1, 2, 5, 6, 11, 1, 5, 7, 12, 3, 11, 8, 5]),
  ]
  test = [
      generate(selected=2, top=1, rows=[1, 1, 10, 7, 3, 10, 10, 12, 13, 13],
               cols=[15, 7, 1, 10, 4, 4, 7, 14, 12, 5]),
  ]
  return {"train": train, "test": test}
