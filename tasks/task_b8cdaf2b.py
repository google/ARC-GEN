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


def generate(neck=None, shoulder=None, shirt=None, antenna=None, b=0):
  """Returns input and output grids according to the given parameters.

  Args:
    neck: the width of the neck
    shoulder: the width of the shoulder
    shirt: the color of the shirt
    antenna: the color of the antenna
    b: the integer used for all background cells
  """
  if neck is None:
    neck = 2 * common.randint(0, 1) + 1
    shoulder = common.randint(1, 3)
    colors = common.random_colors(2)
    shirt, antenna = colors[0], colors[1]

  size = neck + 2 * shoulder
  grid, output = common.grid(size, size, b), common.grid(size, size, b)
  for c in range(shoulder, shoulder + neck):
    output[size - 1][c] = grid[size - 1][c] = antenna
    output[size - 2][c] = grid[size - 2][c] = shirt
  for c in range(shoulder):
    output[size - 1][c] = grid[size - 1][c] = shirt
    output[size - 1][size - 1 - c] = grid[size - 1][size - 1 - c] = shirt
    output[size - 2 - shoulder + c][c] = antenna
    output[size - 2 - shoulder + c][size - 1 - c] = antenna
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(neck=1, shoulder=1, shirt=2, antenna=4),
      generate(neck=1, shoulder=2, shirt=8, antenna=3),
      generate(neck=3, shoulder=1, shirt=6, antenna=1),
      generate(neck=3, shoulder=2, shirt=2, antenna=4),
  ]
  test = [
      generate(neck=3, shoulder=3, shirt=8, antenna=2),
  ]
  return {"train": train, "test": test}
