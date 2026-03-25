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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the pixels.
  """

  if size is None:
    size = 2 * common.randint(1, 4) + 1
    while True:
      colors = common.choices([1, 2, 3, 4, 6, 7, 8, 9], size * (size // 2))
      max_count = max(colors.count(color) for color in colors)
      max_colors = [color for color in set(colors) if colors.count(color) == max_count]
      if len(max_colors) == 1: break

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    output[i // size][i % size] = grid[i // size][i % size] = color
  for c in range(size):
    output[size // 2][c] = grid[size // 2][c] = 5
  max_count = max(colors.count(color) for color in colors)
  max_colors = [color for color in set(colors) if colors.count(color) == max_count]
  output[size - 1][size // 2] = max_colors[0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, colors=[3, 6, 4, 2, 4, 8, 4, 3, 3, 4]),
      generate(size=3, colors=[2, 2, 3]),
      generate(size=7, colors=[1, 9, 9, 6, 1, 8, 4, 4, 6, 7, 8, 9, 7, 1, 9, 3, 1, 4, 1, 3, 6]),
  ]
  test = [
      generate(size=9, colors=[9, 1, 2, 8, 4, 9, 8, 2, 1, 4, 4, 3, 1, 2, 7, 6, 7, 9, 2, 1, 6, 9, 7, 8, 4, 3, 6, 9, 8, 6, 3, 4, 2, 9, 1, 7]),
  ]
  return {"train": train, "test": test}
