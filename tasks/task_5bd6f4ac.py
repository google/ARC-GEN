# Copyright 2025 Google LLC
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


def generate(colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = [common.random_color() for _ in range(size * size * size * size)]
    colors = [c if common.randint(0, 1) else common.black() for c in colors]

  grid = common.grid(size * size, size * size)
  output = common.grid(size, size)
  for r in range(size * size):
    for c in range(size * size):
      grid[r][c] = colors[r * size * size + c]
  for r in range(size):
    for c in range(size):
      output[r][c] = colors[r * size * size + c + 6]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 0, 0, 7, 0, 0, 9, 7, 0, 8, 4, 0, 6, 6, 0, 4, 8, 4, 1,
                       7, 0, 0, 0, 0, 4, 0, 0, 1, 1, 0, 9, 1, 0, 7, 0, 0, 0, 0,
                       0, 0, 7, 7, 0, 0, 0, 8, 0, 0, 1, 7, 0, 8, 4, 0, 0, 7, 0,
                       9, 9, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 2,
                       4, 0, 8, 0, 0]),
      generate(colors=[9, 0, 0, 0, 0, 0, 0, 6, 0, 0, 4, 0, 7, 0, 5, 0, 8, 1, 0,
                       2, 0, 0, 7, 1, 4, 4, 5, 0, 6, 0, 0, 4, 0, 0, 0, 0, 8, 3,
                       0, 4, 2, 0, 0, 9, 7, 0, 0, 2, 3, 0, 2, 0, 6, 7, 4, 0, 4,
                       0, 3, 4, 7, 0, 7, 7, 1, 0, 0, 0, 0, 3, 0, 0, 3, 2, 0, 0,
                       4, 0, 0, 0, 0]),
      generate(colors=[2, 5, 0, 0, 6, 0, 0, 0, 0, 2, 5, 5, 7, 0, 0, 6, 0, 1, 0,
                       3, 0, 0, 0, 1, 9, 4, 0, 0, 7, 0, 6, 0, 0, 0, 0, 0, 0, 9,
                       0, 0, 0, 1, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 0, 5, 0, 0,
                       0, 0, 0, 0, 0]),
      generate(colors=[0, 5, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 2, 1, 0, 0, 3, 0, 1, 0, 0, 0, 0, 3, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 9, 4, 0, 0, 0, 0, 0, 3, 0, 7, 0,
                       0, 2, 0, 0, 6]),
  ]
  test = [
      generate(colors=[6, 9, 0, 0, 1, 0, 5, 8, 9, 2, 9, 0, 6, 0, 8, 0, 9, 0, 0,
                       0, 0, 0, 0, 9, 9, 2, 0, 9, 2, 6, 0, 0, 8, 0, 6, 8, 7, 7,
                       4, 0, 7, 0, 9, 0, 0, 0, 0, 7, 0, 0, 1, 5, 7, 4, 4, 1, 0,
                       0, 7, 5, 0, 0, 9, 9, 9, 0, 0, 0, 0, 1, 0, 0, 4, 9, 2, 0,
                       0, 0, 8, 4, 0]),
  ]
  return {"train": train, "test": test}
