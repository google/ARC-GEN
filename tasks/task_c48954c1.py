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
    num_colors = common.randint(3, 4)
    hues = common.random_colors(num_colors)
    while True:
      colors = common.choices(hues, 9)
      if len(set(colors)) == num_colors: break

  grid, output = common.grid(3, 3), common.grid(9, 9)
  for row in range(3):
    for col in range(3):
      grid[row][col] = colors[3 * row + col]
      for r in range(3):
        for c in range(3):
          rr = (3 * row + r) if row % 2 else (3 * row + 2 - r)
          cc = (3 * col + c) if col % 2 else (3 * col + 2 - c)
          output[rr][cc] = colors[3 * r + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[6, 1, 7, 1, 6, 7, 4, 7, 4]),
      generate(colors=[7, 6, 7, 2, 7, 6, 1, 2, 7]),
      generate(colors=[1, 9, 4, 9, 1, 6, 6, 9, 4]),
  ]
  test = [
      generate(colors=[8, 8, 6, 6, 3, 6, 6, 8, 8]),
  ]
  return {"train": train, "test": test}
