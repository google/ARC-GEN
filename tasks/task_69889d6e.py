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

import common


def generate(vals=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: A list of integers.
  """

  if vals is None:
    vals = [common.randint(0, 1) for _ in range(common.randint(7, 10))]

  grid, output = common.grids(10, 10)
  row, col = 9, 10 - len(vals)
  grid[row][col] = 2
  for val in vals:
    output[row][col] = 2
    if val == 0:
      row -= 1
      output[row][col] = 2
    else:
      grid[row - 1][col] = output[row - 1][col] = 1
    col += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[0, 0, 1, 0, 0, 0, 0, 0, 0]),
      generate(vals=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(vals=[0, 1, 0, 0, 1, 1, 0, 0, 0, 0]),
      generate(vals=[0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(vals=[0, 0, 1, 1, 0, 0, 1, 0, 0]),
  ]
  return {"train": train, "test": test}
