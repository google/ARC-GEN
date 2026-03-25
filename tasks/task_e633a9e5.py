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
    colors: A list of colors.
  """

  if colors is None:
    colors = [common.random_color() for _ in range(9)]

  grid, output = common.grid(3, 3), common.grid(5, 5)
  for i in range(9):
    output[i // 3 + 1][i % 3 + 1] = grid[i // 3][i % 3] = colors[i]
  output[0][0] = output[0][1] = output[1][0] = output[1][1]
  output[4][4] = output[3][4] = output[4][3] = output[3][3]
  output[0][4] = output[0][3] = output[1][4] = output[1][3]
  output[4][0] = output[3][0] = output[4][1] = output[3][1]
  output[0][2] = output[1][2]
  output[4][2] = output[3][2]
  output[2][0] = output[2][1]
  output[2][4] = output[2][3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 3, 5, 1, 2, 8, 8, 3, 8]),
      generate(colors=[6, 5, 5, 5, 1, 7, 4, 5, 2]),
      generate(colors=[2, 3, 7, 2, 1, 6, 1, 5, 7]),
  ]
  test = [
      generate(colors=[1, 2, 5, 7, 3, 6, 7, 6, 5]),
  ]
  return {"train": train, "test": test}
