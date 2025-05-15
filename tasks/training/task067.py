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


def generate(size=None, colors=None, flip_middle=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    colors: a list of digits representing the colors to be used
    flip_middle: whether to flip the middle figure
  """
  if size is None:
    size = common.randint(2, 5)
    color_list = common.sample(range(10), common.randint(2, 4))
    idxs = [common.randint(0, len(color_list) - 1) for _ in range(size * size)]
    colors = [color_list[idx] for idx in idxs]
    flip_middle = common.randint(0, 1)

  grid, output = common.grid(3 * size, size, 0), common.grid(size, size, 0)
  for r in range(size):
    for c in range(size):
      output[r][c] = grid[r][c + size * 2] = grid[r][c] = colors[r * size + c]
      grid[size - r - 1 if flip_middle else r][size + c] = colors[r * size + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, colors=[4, 5, 1, 5, 5, 5, 1, 5, 4], flip_middle=1),
      generate(size=4, colors=[2, 0, 0, 1, 4, 2, 1, 4, 4, 1, 2, 4, 1, 0, 0, 2],
               flip_middle=0),
      generate(size=2, colors=[2, 1, 2, 3], flip_middle=0),
  ]
  test = [
      generate(size=5,
               colors=[0, 2, 0, 4, 4, 2, 2, 0, 4, 4, 0, 2, 2, 2, 0, 1, 1, 0, 2,
                       2, 1, 1, 0, 2, 0],
               flip_middle=0),
  ]
  return {"train": train, "test": test}
