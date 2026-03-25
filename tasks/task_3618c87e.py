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


def generate(cols=None, size=5):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where towers are placed
    size: the width and height of the (square) grid
  """
  if cols is None:
    towers = common.randint(1, 2)
    while True:
      cols = common.sample(range(size), towers)
      if len(cols) == 1: break
      if abs(cols[0] - cols[1]) > 1: break

  grid, output = common.grids(size, size)
  for c in range(size):
    output[size - 1][c] = grid[size - 1][c] = common.gray()
  for c in cols:
    output[size - 2][c] = grid[size - 2][c] = common.gray()
    output[size - 1][c] = grid[size - 3][c] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[2]),
      generate(cols=[1, 3]),
      generate(cols=[1, 4]),
  ]
  test = [
      generate(cols=[2, 4]),
  ]
  return {"train": train, "test": test}
