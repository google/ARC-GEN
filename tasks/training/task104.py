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


def generate(quadrant=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    quadrant: the quadrant to be filled
    size: the width and height of the (square) grid
  """
  if quadrant is None:
    quadrant = common.randint(0, 3)

  grid, output = common.grid(size, size), common.grid(size * size, size * size)
  grid[0][0] = common.green() if quadrant in [0] else common.black()
  grid[0][1] = common.green() if quadrant in [0, 1] else common.black()
  grid[0][2] = common.green() if quadrant in [1] else common.black()
  grid[1][0] = common.green() if quadrant in [0, 2] else common.black()
  grid[1][1] = common.red()
  grid[1][2] = common.green() if quadrant in [1, 3] else common.black()
  grid[2][0] = common.green() if quadrant in [2] else common.black()
  grid[2][1] = common.green() if quadrant in [2, 3] else common.black()
  grid[2][2] = common.green() if quadrant in [3] else common.black()
  for row in range(size + 1):
    for col in range(size + 1):
      r = row if quadrant in [0, 1] else row + 1
      c = col if quadrant in [0, 1] else col + 1
      c = c if quadrant in [0, 3] else size * size - c - 1
      output[r][c] = common.green()
  for row in range(size + 1):
    for col in range(size + 1):
      r = row + 4 if quadrant in [0, 1] else row + 5
      c = col + 4 if quadrant in [0, 1] else col + 5
      c = c if quadrant in [0, 3] else size * size - c - 1
      output[r][c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(quadrant=0),
      generate(quadrant=3),
  ]
  test = [
      generate(quadrant=1),
  ]
  return {"train": train, "test": test}
