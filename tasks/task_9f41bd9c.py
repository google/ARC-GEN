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


def generate(size=None, sky=None, roof=None, flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    sky: The size of the sky.
    roof: The top of the roof.
    flop: Whether to flop the grid.
  """

  if size is None:
    size = common.randint(15, 18)
    roof = common.randint(1, 7)
    sky = common.randint(roof + 4, size - 2)
    flop = common.randint(0, 1)

  grid, output = common.grids(size, size, 6)
  for row in range(sky):
    for c in range(size):
      output[row][c] = grid[row][c] = 1
  for row in range(roof, roof + 2):
    for col in range(5):
      output[row][col] = grid[row][col] = 5
  for row in range(roof + 2, sky):
    grid[row][0] = grid[row][2] = grid[row][4] = 5
    c = row - roof - 2
    output[row][c] = output[row][c + 2] = output[row][c + 4] = 5
  for col in range(sky - roof - 2, size):
    output[sky][col] = 9
  if flop: grid = common.flop(grid)
  else: output = common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=17, sky=11, roof=4, flop=True),
      generate(size=16, sky=11, roof=6, flop=False),
  ]
  test = [
      generate(size=18, sky=14, roof=3, flop=False),
  ]
  return {"train": train, "test": test}
