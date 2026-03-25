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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    colors = [8 * common.randint(0, 1) for _ in range(36)]

  grid, output = common.grids(6, 6)
  for i, color in enumerate(colors):
    grid[i // 6][i % 6] = color
  for row in range(6):
    for col in range(6):
      if not grid[row][col]: continue
      output[row][col] = 2 if grid[row][col] == grid[5 - row][col] else 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 8, 0, 8, 8, 8,
                       8, 8, 8, 8, 8, 0,
                       8, 0, 8, 0, 8, 0,
                       0, 8, 8, 8, 0, 8,
                       8, 8, 0, 8, 8, 0,
                       8, 8, 0, 0, 0, 8]),
      generate(colors=[8, 8, 0, 8, 8, 0,
                       8, 0, 8, 8, 8, 0,
                       0, 0, 8, 8, 8, 8,
                       0, 8, 0, 0, 8, 8,
                       8, 8, 0, 8, 0, 8,
                       8, 0, 0, 8, 0, 8]),
      generate(colors=[0, 8, 8, 0, 0, 8,
                       8, 8, 8, 0, 0, 0,
                       8, 8, 8, 0, 8, 0,
                       8, 0, 8, 8, 0, 8,
                       8, 8, 0, 0, 0, 0,
                       8, 8, 8, 8, 8, 0]),
      generate(colors=[8, 8, 8, 0, 0, 0,
                       0, 0, 8, 8, 0, 8,
                       0, 8, 0, 0, 0, 0,
                       8, 8, 0, 0, 8, 8,
                       8, 0, 8, 8, 8, 8,
                       0, 0, 0, 0, 8, 8]),
  ]
  test = [
      generate(colors=[0, 0, 0, 8, 0, 8,
                       8, 8, 8, 0, 8, 8,
                       8, 8, 8, 8, 0, 8,
                       8, 0, 0, 0, 8, 8,
                       0, 8, 0, 0, 0, 8,
                       8, 8, 8, 0, 8, 8]),
  ]
  return {"train": train, "test": test}
