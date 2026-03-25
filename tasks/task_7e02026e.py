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

  def draw():
    grid, output = common.grids(12, 12)
    for i, color in enumerate(colors):
      output[i // 12][i % 12] = grid[i // 12][i % 12] = color
    num_matches = 0
    for row in range(1, 11):
      for col in range(1, 11):
        good = True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
          if grid[row + dr][col + dc]: good = False
        if not good: continue
        num_matches += 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
          output[row + dr][col + dc] = 3
    return grid, output, num_matches

  if colors is None:
    expected_matches = common.randint(2, 5)
    while True:
      colors = [8 if common.randint(0, 1) else 0 for _ in range(12 * 12)]
      _, _, num_matches = draw()
      if num_matches == expected_matches: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 0, 8, 8, 8, 8, 0, 8, 0, 8, 8, 8,
                       0, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8,
                       8, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8, 8,
                       0, 8, 0, 0, 8, 8, 0, 0, 0, 8, 0, 0,
                       8, 0, 8, 8, 0, 0, 8, 8, 0, 0, 8, 8,
                       8, 8, 8, 0, 8, 8, 0, 0, 8, 8, 8, 8,
                       8, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0,
                       0, 8, 0, 8, 0, 8, 0, 0, 0, 8, 8, 0,
                       0, 8, 0, 8, 0, 0, 0, 8, 8, 0, 8, 8,
                       8, 8, 8, 8, 0, 0, 0, 0, 8, 0, 8, 0,
                       0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 0,
                       8, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8]),
      generate(colors=[8, 0, 0, 8, 0, 0, 0, 8, 8, 0, 8, 0,
                       8, 0, 8, 0, 0, 0, 8, 0, 0, 8, 0, 0,
                       0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 0, 8,
                       0, 8, 0, 8, 0, 0, 8, 0, 8, 8, 0, 0,
                       8, 0, 0, 8, 0, 0, 0, 8, 8, 8, 0, 0,
                       8, 8, 0, 8, 0, 8, 8, 8, 8, 8, 8, 0,
                       0, 8, 0, 0, 0, 8, 0, 8, 0, 8, 8, 0,
                       0, 8, 8, 8, 8, 0, 0, 8, 0, 0, 8, 8,
                       0, 8, 0, 8, 8, 8, 8, 0, 0, 8, 8, 0,
                       0, 8, 8, 8, 8, 0, 0, 0, 8, 0, 0, 8,
                       8, 0, 8, 0, 0, 0, 0, 0, 8, 8, 0, 0,
                       0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 8, 0]),
      generate(colors=[8, 8, 0, 0, 0, 8, 0, 0, 0, 0, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 8,
                       8, 8, 8, 0, 0, 8, 8, 0, 0, 0, 8, 8,
                       0, 8, 0, 8, 8, 8, 8, 0, 0, 8, 8, 8,
                       0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 8, 8, 0, 8, 0, 8, 8, 0, 0,
                       0, 0, 8, 8, 0, 8, 8, 0, 8, 8, 8, 0,
                       8, 8, 8, 0, 8, 8, 8, 8, 0, 8, 0, 8,
                       8, 8, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8,
                       8, 8, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8,
                       8, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8,
                       8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 0, 8]),
  ]
  test = [
      generate(colors=[8, 0, 8, 8, 8, 8, 8, 0, 8, 0, 8, 0,
                       0, 8, 8, 8, 0, 0, 8, 0, 8, 0, 0, 0,
                       8, 8, 8, 8, 0, 0, 0, 8, 8, 8, 8, 8,
                       8, 0, 0, 0, 8, 0, 8, 8, 0, 0, 8, 0,
                       0, 8, 8, 8, 0, 8, 0, 8, 8, 0, 8, 8,
                       0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0,
                       8, 0, 8, 8, 0, 8, 8, 0, 8, 0, 0, 0,
                       0, 8, 0, 8, 0, 0, 8, 8, 8, 8, 8, 8,
                       0, 0, 0, 8, 8, 0, 0, 8, 0, 8, 0, 0,
                       0, 0, 0, 0, 8, 0, 8, 8, 0, 8, 8, 0,
                       0, 0, 0, 8, 8, 0, 8, 8, 0, 8, 8, 8,
                       8, 8, 8, 0, 8, 0, 0, 0, 0, 8, 8, 8]),
  ]
  return {"train": train, "test": test}
