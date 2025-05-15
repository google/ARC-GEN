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
    colors: A list of colors.
  """
  if colors is None:
    colors = common.random_colors(common.randint(3, 9))

  size = 2 * len(colors)
  grid, output = common.grids(size, size)
  for r in range(len(colors)):
    for c in range(len(colors)):
      grid[r][c] = colors[min(r, c)]
      grid[r][size - 1 - c] = colors[min(r, c)]
      grid[size - 1 - r][c] = colors[min(r, c)]
      grid[size - 1 - r][size - 1 - c] = colors[min(r, c)]
      output[r][c] = colors[len(colors) - 1 - min(r, c)]
      output[r][size - 1 - c] = colors[len(colors) - 1 - min(r, c)]
      output[size - 1 - r][c] = colors[len(colors) - 1 - min(r, c)]
      output[size - 1 - r][size - 1 - c] = colors[len(colors) - 1 - min(r, c)]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 2, 1, 3, 5, 8]),
      generate(colors=[2, 1, 6]),
      generate(colors=[8, 1, 2, 4]),
      generate(colors=[7, 2, 4, 1, 3]),
  ]
  test = [
      generate(colors=[8, 2, 4, 3, 7, 6, 5]),
  ]
  return {"train": train, "test": test}
