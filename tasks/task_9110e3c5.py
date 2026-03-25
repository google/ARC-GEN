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
    color, colors = common.randint(1, 3), []
    for _ in range(49):
      if common.randint(0, 1):
        colors.append(0)
      else:
        colors.append(color if common.randint(0, 1) else common.random_color())

  grid, output = common.grid(7, 7), common.grid(3, 3)
  for i, color in enumerate(colors):
    grid[i // 7][i % 7] = color
  # Find the most common color besides 0.
  flattened = [color for color in common.flatten(grid) if color != 0]
  counts = [flattened.count(color) for color in colors]
  zipped = sorted(zip(counts, colors), key=lambda x: x[0], reverse=True)
  _, colors = [list(x) for x in zip(*zipped)]
  coords = []
  if colors[0] == 1: coords = [(0, 2), (1, 0), (1, 1), (2, 1)]
  if colors[0] == 2: coords = [(1, 0), (1, 1), (1, 2)]
  if colors[0] == 3: coords = [(0, 1), (0, 2), (1, 1), (2, 1)]
  for r, c in coords:
    output[r][c] = 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 0, 1, 0, 7, 0, 0,
                       1, 1, 9, 1, 0, 1, 0,
                       0, 0, 1, 1, 0, 2, 0,
                       0, 0, 0, 0, 3, 0, 1,
                       0, 4, 0, 1, 0, 0, 1,
                       0, 0, 1, 0, 2, 0, 8,
                       0, 0, 1, 0, 7, 3, 1]),
      generate(colors=[0, 3, 0, 3, 5, 3, 0,
                       0, 0, 3, 3, 0, 0, 0,
                       8, 0, 0, 0, 0, 0, 3,
                       3, 4, 3, 9, 3, 0, 3,
                       0, 0, 9, 3, 1, 3, 3,
                       0, 3, 3, 3, 0, 3, 0,
                       0, 0, 0, 0, 0, 0, 3]),
      generate(colors=[0, 0, 2, 0, 1, 5, 3,
                       0, 0, 2, 9, 0, 2, 0,
                       2, 2, 2, 4, 2, 0, 0,
                       0, 2, 0, 2, 7, 2, 0,
                       2, 2, 0, 0, 2, 2, 6,
                       0, 2, 2, 0, 2, 0, 0,
                       5, 0, 4, 2, 0, 2, 2]),
      generate(colors=[2, 0, 0, 2, 2, 0, 5,
                       0, 2, 2, 0, 0, 0, 2,
                       0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 9,
                       0, 9, 0, 0, 0, 0, 2,
                       0, 0, 2, 1, 0, 0, 8,
                       2, 0, 0, 2, 2, 0, 0]),
      generate(colors=[0, 4, 0, 0, 4, 1, 3,
                       3, 3, 4, 3, 0, 3, 7,
                       3, 0, 0, 0, 1, 0, 3,
                       0, 0, 3, 0, 3, 0, 0,
                       3, 0, 0, 3, 3, 0, 3,
                       3, 0, 3, 0, 3, 0, 3,
                       3, 3, 3, 0, 4, 2, 3]),
      generate(colors=[0, 0, 0, 2, 2, 0, 2,
                       0, 2, 2, 9, 2, 2, 0,
                       0, 5, 0, 2, 4, 6, 0,
                       2, 0, 0, 0, 0, 9, 2,
                       0, 0, 0, 2, 2, 0, 0,
                       8, 0, 2, 9, 0, 6, 3,
                       0, 2, 0, 2, 0, 2, 4]),
      generate(colors=[0, 4, 1, 0, 0, 1, 6,
                       0, 0, 1, 0, 0, 0, 0,
                       1, 1, 0, 0, 1, 1, 0,
                       0, 1, 0, 0, 0, 1, 1,
                       0, 0, 1, 0, 0, 2, 0,
                       1, 0, 1, 0, 1, 0, 7,
                       1, 1, 1, 0, 4, 1, 0]),
  ]
  test = [
      generate(colors=[3, 0, 3, 0, 0, 0, 3,
                       3, 0, 9, 5, 0, 0, 5,
                       0, 3, 0, 3, 0, 2, 9,
                       8, 3, 0, 3, 0, 0, 7,
                       0, 3, 5, 0, 0, 3, 3,
                       0, 0, 3, 3, 0, 0, 0,
                       0, 0, 3, 0, 4, 0, 0]),
      generate(colors=[0, 0, 8, 1, 1, 0, 1,
                       5, 1, 1, 0, 1, 1, 0,
                       0, 1, 0, 1, 0, 0, 1,
                       1, 0, 2, 0, 0, 6, 0,
                       6, 0, 1, 1, 5, 0, 0,
                       0, 0, 3, 0, 0, 0, 5,
                       0, 1, 0, 0, 2, 0, 1]),
  ]
  return {"train": train, "test": test}
