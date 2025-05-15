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


def generate(heights=None, order=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    heights: a list of different bar heights in descending order
    order: maps each bar to its order index in the grid (left to right)
    size: the width and height of the (square) grid
  """
  if heights is None:
    bars = common.randint(4, 4)
    heights = sorted(common.sample(range(1, 10), bars), reverse=True)
    order = common.shuffle(range(bars))

  grid, output = common.grids(size, size)
  for bar in range(len(heights)):
    for r in range(size - heights[bar], size):
      c = order[bar] * 2 + 1
      output[r][c] = bar + 1
      grid[r][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(heights=[9, 8, 6, 3], order=[2, 0, 1, 3]),
      generate(heights=[8, 5, 4, 2], order=[3, 1, 2, 0]),
  ]
  test = [
      generate(heights=[8, 7, 5, 3], order=[0, 2, 3, 1]),
  ]
  return {"train": train, "test": test}
