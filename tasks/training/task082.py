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


def generate(width=None, cols=None, colors=None, height=6):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    height: the height of the input grid
  """
  if width is None:
    width, col = common.randint(5, 15), common.randint(1, 2)
    cols, colors = [], []
    while col + 1 < width:
      cols.append(col)
      colors.append(common.random_color())
      col += common.randint(3, 4)

  grid, output = common.grids(width, height)
  for c, color in zip(cols, colors):
    grid[0][c] = color
    for r in range(height):
      output[r][c] = color if r % 2 == 0 else common.black()
      for dc in [-1, 1]:
        output[r][c + dc] = common.black() if r % 2 == 0 else color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, cols=[1, 5], colors=[2, 8]),
      generate(width=7, cols=[1], colors=[4]),
  ]
  test = [
      generate(width=12, cols=[2, 6, 9], colors=[3, 6, 7]),
  ]
  return {"train": train, "test": test}
