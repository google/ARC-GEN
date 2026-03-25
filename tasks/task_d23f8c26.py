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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: a list of digits representing the colors to be used
  """
  if size is None:
    size = 2 * common.randint(1, 4) + 1
    while True:
      colors = []
      for _ in range(size * size):
        colors.append(0 if common.randint(0, 1) else common.random_color())
      if len(set(colors)) > 2: break

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      grid[r][c] = colors[r * size + c]
      if c == size // 2: output[r][c] = colors[r * size + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3,
               colors=[6, 4, 0, 0, 3, 9, 1, 0, 0]),
      generate(size=5,
               colors=[8, 0, 3, 0, 0, 8, 6, 5, 6, 0, 3, 6, 3, 0, 0, 0, 0, 0, 5,
                       9, 5, 0, 9, 0, 0]),
      generate(size=5,
               colors=[3, 0, 4, 0, 0, 3, 0, 4, 7, 0, 0, 6, 0, 0, 7, 0, 0, 8, 0,
                       0, 0, 8, 0, 2, 2]),
  ]
  test = [
      generate(size=7,
               colors=[0, 0, 3, 0, 0, 0, 7, 8, 1, 0, 8, 0, 0, 0, 0, 0, 3, 0, 8,
                       0, 3, 0, 7, 0, 1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 8,
                       6, 0, 0, 0, 0, 8, 0, 6, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
