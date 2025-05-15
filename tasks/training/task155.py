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


def generate(size=None, colors=None, color_list=(1, 2, 3, 4, 7, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: digits representing the colors to be used
  """
  if size is None:
    size = common.randint(4, 8)
    idxs = [common.randint(0, len(color_list) - 1) for _ in range(size * size)]
    colors = [color_list[idx] for idx in idxs]

  grid, output = common.grids(size, size, 0)
  for r in range(size):
    for c in range(size):
      output[size - r - 1][c] = grid[r][c] = colors[r * size + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, colors=[8, 1, 2, 1, 4,
                               4, 4, 2, 4, 8,
                               3, 7, 2, 4, 8,
                               2, 7, 7, 8, 7,
                               8, 7, 7, 4, 8]),
      generate(size=5, colors=[7, 3, 3, 1, 2,
                               1, 8, 2, 4, 1,
                               2, 7, 8, 7, 2,
                               7, 7, 4, 1, 8,
                               8, 1, 7, 7, 1]),
      generate(size=7, colors=[2, 7, 4, 3, 4, 8, 3,
                               2, 3, 7, 1, 2, 3, 3,
                               8, 7, 4, 3, 2, 2, 4,
                               1, 1, 2, 1, 4, 4, 7,
                               2, 4, 3, 1, 1, 4, 1,
                               4, 8, 7, 4, 4, 8, 2,
                               7, 3, 8, 4, 3, 2, 8]),
  ]
  test = [
      generate(size=7, colors=[2, 8, 1, 3, 2, 4, 1,
                               4, 4, 1, 1, 4, 3, 4,
                               1, 1, 1, 1, 4, 7, 3,
                               1, 1, 2, 3, 8, 1, 3,
                               4, 1, 1, 1, 7, 8, 4,
                               3, 2, 8, 4, 1, 8, 4,
                               1, 4, 7, 1, 2, 3, 4]),
  ]
  return {"train": train, "test": test}
