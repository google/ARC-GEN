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


def generate(width=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: width of the grid.
  """

  if width is None:
    width = 2 * common.randint(2, 14) + 1

  grid, output = common.grid(width, 1), common.grid(width, width)
  grid[0][width // 2] = 2
  for r in range(width):
    if 2 * r < width:
      output[r][width // 2 - r] = output[r][width // 2 + r] = 2
    for c in range(width):
      if c > width // 2 - r and c < width // 2 + r:
        if abs(r - c + width // 2) % 4 == 0: output[r][c] = 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5),
      generate(width=13),
      generate(width=7),
  ]
  test = [
      generate(width=17),
  ]
  return {"train": train, "test": test}
