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
    colors: The colors of the input pixels.
  """

  if colors is None:
    raw_colors = common.random_colors(3)
    colors = [raw_colors[common.randint(0, 2)] for _ in range(12)]

  grid, output = common.grid(4, 3), common.grid(8, 6)
  for r in range(3):
    for c in range(4):
      grid[r][c] = colors[r * 4 + c]
      output[r + 3][c + 4] = colors[r * 4 + c]
      output[r + 3][3 - c] = colors[r * 4 + c]
      output[2 - r][c + 4] = colors[r * 4 + c]
      output[2 - r][3 - c] = colors[r * 4 + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 9, 9, 9, 5, 5, 5, 5, 7, 5, 7]),
      generate(colors=[6, 2, 4, 2, 2, 2, 6, 6, 6, 4, 2, 4]),
      generate(colors=[3, 3, 5, 5, 5, 8, 5, 8, 8, 8, 5, 8]),
  ]
  test = [
      generate(colors=[8, 5, 7, 8, 7, 7, 8, 8, 5, 5, 8, 5]),
  ]
  return {"train": train, "test": test}
