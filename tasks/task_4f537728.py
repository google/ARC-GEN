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


def generate(row=None, col=None, color=None, row_offset=None, col_offset=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if row is None:
    row, col = common.randint(1, 5), common.randint(1, 5)
    color = common.random_color(exclude=[1])
    row_offset, col_offset = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(20, 20)
  for r in range(7):
    for c in range(7):
      hue = 1 if row != r or col != c else color
      common.hollow_rect(grid, 2, 2, r * 3 - row_offset, c * 3 - col_offset, hue)
      hue = 1 if row != r and col != c else color
      common.hollow_rect(output, 2, 2, r * 3 - row_offset, c * 3 - col_offset, hue)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=5, col=4, color=3, row_offset=1, col_offset=1),
      generate(row=2, col=2, color=2, row_offset=0, col_offset=0),
  ]
  test = [
      generate(row=2, col=5, color=8, row_offset=1, col_offset=0),
  ]
  return {"train": train, "test": test}
