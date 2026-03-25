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
    colors: The colors of the pixels.
  """

  if colors is None:
    subset = common.random_colors(common.randint(2, 4))
    while True:
      colors = common.choices(subset, 9)
      counts = sorted([colors.count(c) for c in set(colors)])
      if counts.count(counts[0]) == 1: break

  grid, output = common.grid(3, 3), common.grid(9, 9)
  for i, color in enumerate(colors):
    grid[i // 3][i % 3] = color
  min_color = sorted([(colors.count(c), c) for c in set(colors)])[0][1]
  for row in range(3):
    for col in range(3):
      if colors[row * 3 + col] != min_color: continue
      for i, color in enumerate(colors):
        output[3 * row + i // 3][3 * col + i % 3] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 2, 7, 2, 2, 7, 5, 5, 7]),
      generate(colors=[8, 5, 5, 8, 8, 8, 5, 9, 9]),
      generate(colors=[7, 1, 7, 1, 7, 7, 7, 1, 7]),
      generate(colors=[1, 6, 6, 5, 1, 6, 5, 5, 5]),
      generate(colors=[9, 9, 6, 3, 8, 8, 8, 3, 3]),
      generate(colors=[4, 4, 2, 2, 2, 2, 2, 4, 2]),
  ]
  test = [
      generate(colors=[9, 7, 9, 9, 9, 7, 7, 9, 7]),
  ]
  return {"train": train, "test": test}
