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


def generate(vals=None, offset=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    vals: a list of bar heights
    offset: the amount to shift bars horizontally
    size: the width and height of the (square) grid
  """
  if offset is None:
    offset = common.randint(0, 1)
    num = common.randint(4, 4 if offset == 1 else 5)
    vals = common.sample(range(1, size + 1), num)

  grid, output = common.grids(size, size)
  for idx, val in enumerate(vals):
    for c in range(val):
      grid[size - 1 - c][2 * idx + offset] = common.gray()
      if val == min(vals):
        output[size - 1 - c][2 * idx + offset] = common.red()
      elif val == max(vals):
        output[size - 1 - c][2 * idx + offset] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vals=[6, 8, 4, 7, 3], offset=0),
      generate(vals=[7, 2, 9, 6], offset=0),
  ]
  test = [
      generate(vals=[1, 7, 5, 8], offset=1),
  ]
  return {"train": train, "test": test}
