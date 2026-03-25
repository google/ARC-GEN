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


def generate(length=None, color=None, flip=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    length: The length of the lines.
    color: The color of the lines.
    flip: Whether to flip the grids.
    flop: Whether to flop the grids.
  """

  if length is None:
    length = common.randint(2, 6)
    color = common.random_color(exclude=[7])
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grid(6, 6, 7), common.grid(16, 16, 7)
  for i in range(length):
    grid[0][i] = grid[i][0] = color
  for i in range(2 * length):
    output[0][i] = output[i][0] = output[i][2 * length - 1 - i] = color
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(length=2, color=5, flip=1, flop=1),
      generate(length=3, color=9, flip=1, flop=0),
  ]
  test = [
      generate(length=4, color=8, flip=0, flop=1),
  ]
  return {"train": train, "test": test}
