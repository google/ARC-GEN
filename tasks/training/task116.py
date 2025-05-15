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


def generate(rows=None, cols=None, b=None, color=None, width=4, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    b: the integer used for all background cells
    color: a digit representing a color to be used
    width: the width of the input grid
    height: the height of the input grid
  """
  if rows is None:
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)
    colors = common.random_colors(2)
    b, color = colors[0], colors[1]

  grid = common.grid(width, height, b)
  output = common.grid(width, 2 * height, b)
  for r, c in zip(rows, cols):
    output[height + r][c] = output[height - 1 - r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2], cols=[2, 0, 1, 1], b=9, color=5),
      generate(rows=[0, 0, 1, 1, 1, 1, 2], cols=[1, 2, 0, 1, 2, 3, 3], b=4,
               color=1),
      generate(rows=[0, 0, 1, 1], cols=[0, 2, 0, 1], b=4, color=9),
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[0, 1, 0, 3, 2, 3], b=5, color=3),
  ]
  test = [
      generate(rows=[0, 0, 2, 2], cols=[2, 3, 2, 3], b=4, color=9),
  ]
  return {"train": train, "test": test}
