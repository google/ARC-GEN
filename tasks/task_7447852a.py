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


def generate(width=None, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
  """
  if width is None:
    width = common.randint(5, 25)

  grid, output = common.grids(width, height)
  mode = -1
  for c in range(width):
    r = c % (2 * height - 2)
    r = r if r < height else 2 * height - r - 2
    output[r][c] = grid[r][c] = common.red()
    mode = mode if r not in [0, height - 1] else (mode + 1) % 6
    if mode in [0, 5]:
      for i in range(r + 1, height):
        output[i][c] = common.yellow()
    if mode in [2, 3]:
      for i in range(0, r):
        output[i][c] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10),
      generate(width=15),
      generate(width=18),
  ]
  test = [
      generate(width=25),
  ]
  return {"train": train, "test": test}
