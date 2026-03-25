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


def generate(rows=None, left_colors=None, right_colors=None, width=11,
             height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where lines sholud be placed
    left_colors: which colors to use for the left side
    right_colors: which colors to use for the right side
    width: the width of the grid
    height: the height of the grid
  """
  if rows is None:
    num = common.randint(1, 2)
    rows = common.sample(range(height), num)
    colors = list(range(1, 10))
    colors.remove(common.gray())
    colors = common.shuffle(colors)
    left_colors, right_colors = colors[0:num], colors[num:2*num]

  grid, output = common.grids(width, height)
  for r, left_color, right_color in zip(rows, left_colors, right_colors):
    grid[r][0], grid[r][-1] = left_color, right_color
    for c in range(width // 2):
      output[r][c], output[r][width - 1 - c] = left_color, right_color
    output[r][width // 2] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1], left_colors=[1], right_colors=[2]),
      generate(rows=[3], left_colors=[3], right_colors=[7]),
  ]
  test = [
      generate(rows=[1, 4], left_colors=[4, 6], right_colors=[8, 9]),
  ]
  return {"train": train, "test": test}
