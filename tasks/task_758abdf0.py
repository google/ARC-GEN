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


def generate(lengths=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: The lengths of the lines.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  if lengths is None:
    lengths = []
    for _ in range(16):
      lengths.append(0 if lengths and lengths[-1] else common.randint(0, 2))
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(8, 16, 7)
  for row in range(16):
    output[row][0] = grid[row][0] = 0
    if lengths[row] == 1:
      output[row][2] = output[row][1] = grid[row][1] = 8
    if lengths[row] == 2:
      grid[row][1] = grid[row][2] = 8
      output[row][6] = output[row][7] = 0
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1], flip=False, xpose=False),
      generate(lengths=[0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], flip=False, xpose=True),
  ]
  test = [
      generate(lengths=[2, 0, 1, 0, 2, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 2], flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
