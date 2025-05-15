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


def generate(colors=None, color_list=(2, 3, 4, 8)):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: the colors to be used for the output grid
    color_list: the available list of colors for the output grid
  """
  if colors is None:
    colors = [color_list[common.randint(0, 3)] for _ in range(3)]

  grid, output = common.grid(14, 4), common.grid(3, 3)
  for idx in range(3):
    for r in range(4):
      for c in range(4):
        grid[r][idx * 5 + c] = common.gray()
  for idx in range(3):
    if colors[idx] == 8:
      grid[1][idx * 5 + 1] = grid[1][idx * 5 + 2] = common.black()
      grid[2][idx * 5 + 1] = grid[2][idx * 5 + 2] = common.black()
    elif colors[idx] == 3:
      grid[1][idx * 5] = grid[1][idx * 5 + 3] = common.black()
      grid[2][idx * 5] = grid[2][idx * 5 + 3] = common.black()
    elif colors[idx] == 4:
      grid[2][idx * 5 + 1] = grid[2][idx * 5 + 2] = common.black()
      grid[3][idx * 5 + 1] = grid[3][idx * 5 + 2] = common.black()
  for r in range(3):
    for c in range(3):
      output[r][c] = colors[r]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 8, 3]),
      generate(colors=[3, 4, 2]),
      generate(colors=[8, 2, 4]),
      generate(colors=[2, 4, 2]),
  ]
  test = [
      generate(colors=[4, 3, 8]),
  ]
  return {"train": train, "test": test}
