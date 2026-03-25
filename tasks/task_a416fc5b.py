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


def generate(index=None, invert=None):
  """Returns input and output grids according to the given parameters.

  Args:
    index: The index of the red sprite.
    invert: Whether to invert the grids.
  """

  row_map = [-1, -1, -1, 0, 1, 1, 1, 0]
  col_map = [-1, 0, 1, 1, 1, 0, -1, -1]

  if index is None:
    index, invert = common.randint(0, 7), common.randint(0, 1)

  def get_grey_coord():
    idx = (index + 3) % 8
    return row_map[idx], col_map[idx]

  def get_blue_coord():
    idx = (index + 5) % 8
    return row_map[idx], col_map[idx]

  grid, output = common.grids(11, 11, 7)
  for i in range(11):
    for j in range(3, 11, 4):
      output[i][j] = output[j][i] = grid[i][j] = grid[j][i] = 6
  for r, c in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
    drow, dcol = row_map[index], col_map[index]
    grow, gcol = get_grey_coord()
    brow, bcol = get_blue_coord()
    for g in [grid, output]:
      g[5 + r][5 + c] = g[5 + r + 4 * drow][5 + c + 4 * dcol] = 2
    output[5 + r + 4 * grow][5 + c + 4 * gcol] = 5
    output[5 + r + 4 * brow][5 + c + 4 * bcol] = 8
  if invert: grid, output = output, common.grid(16, 16, 7)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(index=5, invert=False),
      generate(index=2, invert=False),
      generate(index=0, invert=True),
  ]
  test = [
      generate(index=3, invert=False),
  ]
  return {"train": train, "test": test}
