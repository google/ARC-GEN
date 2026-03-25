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


def generate(colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = [common.randint(0, 3) for _ in range(size * size)]

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c] = colors[r * size + c]
      output[2 * size - 1 - r][c] = colors[r * size + c]
      output[r][2 * size - 1 - c] = colors[r * size + c]
      output[2 * size - 1 - r][2 * size - 1 - c] = colors[r * size + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 3, 3, 0, 2, 2, 1, 1, 0]),
      generate(colors=[3, 3, 1, 1, 3, 0, 0, 2, 2]),
      generate(colors=[2, 1, 0, 0, 2, 3, 0, 3, 0]),
  ]
  test = [
      generate(colors=[1, 1, 0, 0, 3, 2, 3, 3, 0]),
  ]
  return {"train": train, "test": test}
