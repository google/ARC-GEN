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
    subset = common.random_colors(common.randint(1, 3), exclude=[8])
    while True:
      colors = [common.randint(0, 2) for _ in range(9)]
      colors = [8 if color else common.choice(subset) for color in colors]
      if len(set(colors)) == len(subset) + 1: break

  grid, output = common.grid(3, 3), common.grid(12, 12)
  for row in range(3):
    for col in range(3):
      grid[row][col] = colors[row * 3 + col]
      for r in range(4):
        for c in range(4):
          if r > 1 and c > 1:
            rr = r * 3 + row
            cc = c * 3 + col
          elif r < 2 and c > 1:
            rr = c * 3 + 2 - col
            cc = r * 3 + row
          elif r > 1 and c < 2:
            rr = c * 3 + col
            cc = r * 3 + 2 - row
          else:
            rr = r * 3 + 2 - row
            cc = c * 3 + 2 - col
          output[rr][cc] = colors[row * 3 + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[8, 7, 8, 7, 8, 8, 8, 5, 1]),
      generate(colors=[6, 8, 8, 8, 6, 8, 8, 8, 8]),
      generate(colors=[1, 8, 8, 8, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(colors=[8, 8, 8, 8, 8, 2, 8, 6, 4]),
  ]
  return {"train": train, "test": test}
