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
    grid = common.grid(10, 9)
    for row in range(2):
      for col in range(3):
        subset = common.random_colors(2)
        while True:
          block = common.choices(subset, 6)
          if block.count(subset[0]) in [1, 2]: break
        for r in range(3):
          for c in range(2):
            grid[row * 4 + 1 + r][col * 3 + 1 + c] = block[r * 2 + c]
    colors = common.flatten(grid)

  grid, output = common.grid(10, 9), common.grid(5, 4)
  for i, color in enumerate(colors):
    grid[i // 10][i % 10] = color
  for row in range(2):
    for col in range(3):
      colors = []
      for r in range(3):
        for c in range(2):
          colors.append(grid[row * 4 + 1 + r][col * 3 + 1 + c])
      counts = {c: colors.count(c) for c in colors}
      output[row + 1][col + 1] = max(counts, key=counts.get)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 0, 5, 5, 0, 4, 4, 0,
                       0, 1, 1, 0, 3, 3, 0, 4, 4, 0,
                       0, 3, 3, 0, 5, 5, 0, 4, 8, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 7, 1, 0, 9, 9, 0,
                       0, 2, 2, 0, 7, 7, 0, 1, 9, 0,
                       0, 2, 2, 0, 7, 1, 0, 9, 9, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 6, 6, 0, 9, 7, 0,
                       0, 8, 3, 0, 6, 3, 0, 9, 7, 0,
                       0, 3, 8, 0, 3, 6, 0, 7, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 2, 2, 0, 6, 1, 0,
                       0, 2, 3, 0, 5, 5, 0, 1, 1, 0,
                       0, 2, 3, 0, 5, 5, 0, 1, 6, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 5, 0, 8, 4, 0, 7, 7, 0,
                       0, 5, 3, 0, 8, 8, 0, 7, 6, 0,
                       0, 3, 3, 0, 8, 4, 0, 6, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 2, 2, 0, 1, 3, 0,
                       0, 4, 3, 0, 2, 2, 0, 1, 1, 0,
                       0, 3, 3, 0, 1, 2, 0, 1, 3, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 0, 3, 3, 0, 4, 4, 0,
                       0, 3, 1, 0, 8, 3, 0, 4, 4, 0,
                       0, 1, 1, 0, 3, 8, 0, 8, 4, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 0, 3, 5, 0, 2, 2, 0,
                       0, 6, 6, 0, 5, 5, 0, 2, 2, 0,
                       0, 2, 2, 0, 5, 3, 0, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
