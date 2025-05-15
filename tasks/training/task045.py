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


def generate(colors=None, shuffled=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing different colors
    shuffled: a list of those same colors in a shuffled order
    size: the width and height of the (square) grid
  """
  if colors is None:
    lines = common.randint(4, 5)
    colors = common.random_colors(lines)
    shuffled = common.sample(colors, lines)

  grid, output = common.grids(size, size)
  for idx in range(len(colors)):
    r = 2 * idx + 1
    output[r][0] = grid[r][0] = colors[idx]
    output[r][size - 1] = grid[r][size - 1] = shuffled[idx]
    if colors[idx] != shuffled[idx]: continue
    for c in range(0, size):
      output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[9, 8, 4, 6], shuffled=[6, 9, 4, 8]),
      generate(colors=[8, 4, 3, 1, 2], shuffled=[8, 2, 4, 1, 3]),
      generate(colors=[2, 3, 5, 8], shuffled=[8, 4, 3, 2]),
  ]
  test = [
      generate(colors=[4, 3, 2, 6, 9], shuffled=[2, 3, 9, 6, 4]),
  ]
  return {"train": train, "test": test}
