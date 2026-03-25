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
    while True:
      colors = common.random_colors(4)
      colors = [color if color != 7 else 0 for color in colors]
      colors = [color if common.randint(0, 1) else 7 for color in colors]
      if len(set(colors)) > 1: break

  grid, output = common.grids(8, 8, 7)
  grid[0][0] = colors[0]
  grid[0][7] = colors[1]
  grid[7][0] = colors[2]
  grid[7][7] = colors[3]
  output[1][1] = output[1][2] = output[2][1] = output[2][2] = colors[0]
  output[1][5] = output[1][6] = output[2][5] = output[2][6] = colors[1]
  output[4][2] = output[5][2] = output[6][3] = colors[2]
  output[4][5] = output[5][5] = output[6][4] = colors[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 7, 1, 7]),
      generate(colors=[7, 8, 7, 7]),
      generate(colors=[7, 7, 7, 0]),
      generate(colors=[9, 7, 7, 7]),
  ]
  test = [
      generate(colors=[2, 5, 8, 4]),
  ]
  return {"train": train, "test": test}
