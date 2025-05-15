# Copyright 2025 Google LLC
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


def generate(rows=None, cols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows = [item for item in range(1, size) if common.randint(0, 1) == 0]
    cols = [item for item in range(0, size - 1) if common.randint(0, 1) == 0]

  grid, output = common.grids(size, size)
  for c in cols:
    output[0][c] = grid[0][c] = common.gray()
  for r in rows:
    output[r][size - 1] = grid[r][size - 1] = common.gray()
  for c in cols:
    for r in rows:
      output[r][c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 7], cols=[0, 3, 7]),
      generate(rows=[2, 4, 7], cols=[1, 3, 4, 7]),
      generate(rows=[2, 3, 6, 8], cols=[2, 3, 5, 7, 8]),
  ]
  test = [
      generate(rows=[2, 3, 5, 7, 9], cols=[0, 2, 3, 6, 8]),
  ]
  return {"train": train, "test": test}
