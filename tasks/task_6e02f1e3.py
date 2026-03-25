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


def generate(idxs=None, color_offset=2, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    idxs: a list of indices into the color list
    color_offset: how much to add to the index values
    size: the width and height of the (square) grid
  """
  if idxs is None:
    colors = common.sample([0, 1, 2], common.randint(1, 3))
    max_color = len(colors) - 1
    idxs = [colors[common.randint(0, max_color)] for _ in range(size * size)]

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      grid[r][c] = idxs[r * size + c] + color_offset
  num_colors = len(set(idxs))
  if num_colors == 1:
    output[0][0] = output[0][1] = output[0][2] = common.gray()
  if num_colors == 2:
    output[0][0] = output[1][1] = output[2][2] = common.gray()
  if num_colors == 3:
    output[0][2] = output[1][1] = output[2][0] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(idxs=[0, 0, 0, 1, 0, 1, 1, 1, 1]),
      generate(idxs=[1, 1, 1, 2, 0, 0, 2, 2, 0]),
      generate(idxs=[2, 2, 2, 2, 2, 2, 2, 2, 2]),
      generate(idxs=[1, 1, 1, 1, 1, 1, 1, 1, 1]),
      generate(idxs=[2, 2, 2, 2, 2, 2, 1, 1, 1]),
  ]
  test = [
      generate(idxs=[2, 2, 2, 0, 1, 0, 1, 0, 1]),
  ]
  return {"train": train, "test": test}
