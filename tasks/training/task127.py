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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
  """
  if colors is None:
    colors = [common.randint(1, 4) for _ in range(3 * common.randint(1, 2))]

  width, height = 11, 4 * len(colors) // 3 - 1
  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(3, width, 4):
      output[r][c] = grid[r][c] = common.gray()
  for r in range(3, height, 4):
    for c in range(width):
      output[r][c] = grid[r][c] = common.gray()
  for idx, color in enumerate(colors):
    r, c = idx // 3, idx % 3
    grid[4 * r + 1][4 * c + 1] = color
    for dr in range(3):
      for dc in range(3):
        output[4 * r + dr][4 * c + dc] = color + 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 2, 1]),
      generate(colors=[2, 3, 1]),
      generate(colors=[3, 1, 4]),
      generate(colors=[4, 1, 2, 2, 3, 4]),
  ]
  test = [
      generate(colors=[2, 3, 4, 1, 1, 3]),
  ]
  return {"train": train, "test": test}
