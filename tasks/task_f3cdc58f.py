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
    while True:
      colors = [0] * 100
      for color in range(1, 5):
        for _ in range(common.randint(2, 8)):
          colors[common.randint(0, 99)] = color
      good = True
      for color in range(1, 5):
        if not colors.count(color): good = False
      if good: break

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    grid[i // 10][i % 10] = color
  for color in range(1, 5):
    for r in range(colors.count(color)):
      output[9 - r][color - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 4, 0, 3, 3, 0, 0, 1, 3, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 3, 0, 0, 0, 2, 0, 0, 0,
                       2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 4,
                       3, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0,
                       4, 0, 1, 0, 1]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                       0, 2, 0, 0, 0, 0, 3, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0,
                       0, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 0, 4,
                       0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0,
                       0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0, 4,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 0,
                       0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                       0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 2, 4, 0, 0,
                       0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 3, 4, 0, 0, 1, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 0, 1, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 2,
                       4, 0, 2, 4, 2]),
  ]
  return {"train": train, "test": test}
