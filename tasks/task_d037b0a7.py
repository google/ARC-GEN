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


def generate(rows=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    colors: digits representing colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows = [common.randint(0, size - 1) for _ in range(size)]
    colors = common.sample(range(10), size)

  grid, output = common.grids(size, size)
  for c, row in enumerate(rows):
    grid[row][c] = colors[c]
    for r in range(row, size):
      output[r][c] = colors[c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 1, 0], colors=[3, 4, 6]),
      generate(rows=[1, 0, 1], colors=[7, 2, 8]),
      generate(rows=[0, 1, 2], colors=[4, 2, 0]),
  ]
  test = [
      generate(rows=[0, 2, 0], colors=[4, 7, 8]),
  ]
  return {"train": train, "test": test}
