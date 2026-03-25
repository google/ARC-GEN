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
    hue = common.random_color()
    while True:
      colors = [hue * common.randint(0, 1) for _ in range(9)]
      if len(set(colors)) == 2: break

  grid, output = common.grid(3, 3), common.grid(6, 6)
  for row in range(3):
    for col in range(3):
      grid[row][col] = colors[row * 3 + col]
      output[row][col] = colors[row * 3 + col]
      output[2 - col][row + 3] = colors[row * 3 + col]
      output[col + 3][5 - row] = colors[row * 3 + col]
      output[5 - row][2 - col] = colors[row * 3 + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 0, 8, 8, 0, 0, 8, 0, 0]),
      generate(colors=[3, 0, 3, 0, 3, 3, 3, 3, 3]),
      generate(colors=[3, 3, 3, 0, 0, 3, 3, 0, 0]),
      generate(colors=[0, 7, 7, 0, 0, 0, 7, 7, 0]),
      generate(colors=[9, 9, 9, 0, 0, 0, 9, 9, 0]),
  ]
  test = [
      generate(colors=[6, 6, 0, 6, 6, 0, 0, 0, 6]),
  ]
  return {"train": train, "test": test}
