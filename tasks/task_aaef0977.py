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


def generate(row=None, col=None, index=None):
  """Returns input and output grids according to the given parameters.

  Args:
    row: The row index of the pixel.
    col: The column index of the pixel.
    index: The index of the pixel.
  """

  colors = [0, 5, 2, 8, 9, 6, 1, 3, 4]
  if index is None:
    index = common.randint(0, 8)
    row, col = common.randint(0, 7), common.randint(0, 7)

  grid, output = common.grids(8, 8, 7)
  grid[row][col] = colors[index]
  for r in range(8):
    for c in range(8):
      output[r][c] = colors[(index + abs(r - row) + abs(c - col)) % 9]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=0, col=6, index=7),
      generate(row=5, col=2, index=1),
  ]
  test = [
      generate(row=2, col=1, index=0),
  ]
  return {"train": train, "test": test}
