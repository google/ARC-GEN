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


def generate(width=None, height=None, colors=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    colors: a list of digits representing the color of each pixel
    rows: a list of vertical coordinates where centers should be placed
    cols: a list of horizontal coordinates where centers should be placed
  """
  if width is None:
    width, height = common.randint(6, 15), common.randint(6, 15)
    colors = []
    for color in [2, 1, 3]:
      colors.extend([color for _ in range(common.randint(1, 2))])
    rows = common.sample(range(height), len(colors))
    cols = [common.randint(0, width - 1) for _ in colors]

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = grid[r][c] = color
    if color == 2:  # red lines go up
      for i in range(height):
        output[i][c] = 2
    if color in [1, 3]:  # blue and green lines go across
      for i in range(width):
        output[r][i] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=9, colors=[2, 1, 3], rows=[2, 6, 4],
               cols=[2, 3, 7]),
      generate(width=8, height=10, colors=[2, 1, 3, 3], rows=[7, 6, 1, 4],
               cols=[5, 1, 1, 3]),
      generate(width=11, height=10, colors=[2, 2, 1, 3, 3],
               rows=[8, 9, 1, 3, 6], cols=[3, 9, 1, 8, 2]),
  ]
  test = [
      generate(width=11, height=12, colors=[2, 2, 1, 1, 3, 3],
               rows=[1, 5, 7, 9, 0, 3], cols=[9, 4, 1, 8, 3, 5]),
  ]
  return {"train": train, "test": test}
