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


def generate(rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
  """

  if rows is None:
    rows = common.sample(range(1, 12), 3)
    cols = common.sample(range(1, 12), 3)

  grid, output = common.grids(13, 13)
  for i in range(3):
    output[rows[i]][cols[i]] = grid[rows[i]][cols[i]] = i + 2
  for left, right in [(0, 2), (2, 1)]:
    col_diff = 1 if cols[right] > cols[left] else -1
    while cols[left] != cols[right]:
      cols[left] += col_diff
      output[rows[left]][cols[left]] = 5
    row_diff = 1 if rows[right] > rows[left] else -1
    while rows[left] != rows[right]:
      output[rows[left]][cols[left]] = 5
      rows[left] += row_diff
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[10, 4, 1], cols=[5, 11, 1]),
      generate(rows=[8, 1, 10], cols=[11, 5, 2]),
      generate(rows=[5, 11, 1], cols=[2, 9, 10]),
      generate(rows=[2, 11, 6], cols=[1, 3, 10]),
  ]
  test = [
      generate(rows=[5, 11, 2], cols=[1, 7, 10]),
  ]
  return {"train": train, "test": test}
