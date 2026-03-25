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


def generate(tops=None, bottoms=None, col=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    tops: a list of column sizes for the tops
    bottoms: a list of column sizes for the bottoms
    col: how much space to leave on the left side
    size: the width and height of the (square) grid
  """
  if tops is None:
    col, loc = common.randint(1, 3), common.randint(1, 3)
    tops, bottoms = [], []
    for _ in range(col, size - loc):
      top = common.randint(1, 5)
      bottom = 0 if top >= 4 else common.randint(1, 6)
      tops.append(top)
      bottoms.append(bottom)

  grid, output = common.grids(size, size)
  for idx in range(len(tops)):
    top, bottom = tops[idx], bottoms[idx]
    for r in range(top):
      output[r][col + idx] = grid[r][col + idx] = common.blue()
    for r in range(bottom):
      output[top + r][col + idx] = grid[size - r - 1][col + idx] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tops=[4, 4, 2, 4, 4], bottoms=[0, 0, 3, 0, 0], col=2),
      generate(tops=[4, 4, 1, 4, 2, 5, 5], bottoms=[0, 0, 1, 0, 4, 0, 0],
               col=2),
      generate(tops=[4, 4, 1, 3, 4, 3, 4, 2, 4],
               bottoms=[0, 0, 3, 2, 0, 4, 0, 3, 0], col=1),
  ]
  test = [
      generate(tops=[4, 1, 5, 2, 3, 2, 4, 1, 5],
               bottoms=[0, 3, 0, 2, 4, 1, 0, 6, 0], col=1),
  ]
  return {"train": train, "test": test}
