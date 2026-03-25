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


def generate(rows=None, cols=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows = common.sample(range(1, size - 2), 2)
    cols = common.sample(range(1, size - 2), 2)

  grid, output = common.grids(size, size)
  grid[rows[0]][cols[0]] = common.cyan()
  grid[rows[1]][cols[1]] = common.orange()
  for r in range(size):
    output[r][cols[0]] = common.cyan()
    output[r][cols[1]] = common.orange()
  for c in range(size):
    output[rows[0]][c] = common.cyan()
    output[rows[1]][c] = common.orange()
  output[rows[0]][cols[1]] = output[rows[1]][cols[0]] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 6], cols=[2, 6]),
      generate(rows=[1, 7], cols=[3, 6]),
  ]
  test = [
      generate(rows=[1, 6], cols=[4, 1]),
  ]
  return {"train": train, "test": test}
