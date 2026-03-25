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
    colors = common.choices([2, 2, 2, 2, 5, 5, 5, 5, 7], common.randint(3, 12))

  width, height = len(colors), (len(colors) + 1) // 2
  grid, output = common.grids(width, height, 7)
  for c, color in enumerate(colors):
    output[0][c] = grid[0][c] = color
  for r in range(1, height):
    for c in range(1, width - 1):
      if output[r - 1][c - 1] != 7 and output[r - 1][c + 1] != 7:
        output[r][c] = 7 - output[r - 1][c - 1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 5, 7, 2, 7]),
      generate(colors=[7, 2, 7, 2, 7]),
      generate(colors=[2, 5, 2, 5, 2]),
      generate(colors=[7, 2, 7, 5, 7]),
      generate(colors=[5, 5, 2, 2, 5, 5, 5, 2, 2]),
      generate(colors=[7, 5, 7, 5, 7]),
      generate(colors=[5, 2, 5, 5, 5, 5, 2]),
  ]
  test = [
      generate(colors=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7]),
  ]
  return {"train": train, "test": test}
