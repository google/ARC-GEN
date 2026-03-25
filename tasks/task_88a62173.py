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


def generate(same=None, diff=None, idx=None, color=None, size=5):
  """Returns input and output grids according to the given parameters.

  Args:
    same: a list of pixel indices for the "same" sprites
    diff: a list of pixel indices for the "different" sprite
    idx: the cell where the different sprite should live
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if same is None:
    while True:
      same = common.sample(range(4), common.randint(2, 3))
      diff = common.sample(range(4), common.randint(2, 3))
      if set(same) != set(diff): break
    idx = common.randint(0, 3)
    color = common.random_color()

  grid, output = common.grid(size, size), common.grid(2, 2)
  for i, r, c in zip(range(4), [0, 0, 1, 1], [0, 1, 0, 1]):
    the_list = diff if i == idx else same
    if 0 in the_list:
      grid[3 * r][3 * c] = color
    if 1 in the_list:
      grid[3 * r][3 * c + 1] = color
    if 2 in the_list:
      grid[3 * r + 1][3 * c] = color
    if 3 in the_list:
      grid[3 * r + 1][3 * c + 1] = color
  if 0 in diff:
    output[0][0] = color
  if 1 in diff:
    output[0][1] = color
  if 2 in diff:
    output[1][0] = color
  if 3 in diff:
    output[1][1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(same=[1, 2, 3], diff=[0, 1, 2], idx=3, color=2),
      generate(same=[0, 3], diff=[0, 2, 3], idx=2, color=1),
      generate(same=[0, 1, 2], diff=[1, 2], idx=1, color=8),
  ]
  test = [
      generate(same=[0, 1, 3], diff=[0, 3], idx=1, color=5),
  ]
  return {"train": train, "test": test}
