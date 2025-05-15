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
    size = common.randint(3, 5)
    colors = [common.random_color() for _ in range(size * size)]
    for idx in range(len(colors)):
      if common.randint(0, 1): continue
      colors[idx] = common.choice([common.gray(), common.cyan()])

  grid, output = common.grids(size, size, 0)
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c] = colors[r * size + c]
      if grid[r][c] == common.gray(): output[r][c] = common.cyan()
      if grid[r][c] == common.cyan(): output[r][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5,
               colors=[2, 7, 8, 8, 8, 5, 5, 6, 5, 4, 8, 5, 5, 5, 2, 8, 8, 4, 3,
                       6, 6, 5, 1, 9, 3]),
      generate(size=3, colors=[3, 5, 1, 4, 5, 8, 2, 4, 9]),
      generate(size=3, colors=[6, 5, 3, 5, 7, 5, 8, 8, 2]),
  ]
  test = [
      generate(size=4, colors=[8, 8, 4, 5, 3, 8, 7, 5, 3, 7, 1, 9, 6, 4, 8, 8]),
  ]
  return {"train": train, "test": test}
