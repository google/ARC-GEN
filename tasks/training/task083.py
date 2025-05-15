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


def generate(rows=None, cols=None, color=None, width=4, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width of the folded grid
    height: the width of the folded grid
  """
  if rows is None:
    pixels = common.random_pixels(width, height)
    rows, cols = zip(*pixels)
    color = common.random_color()

  grid, output = common.grid(width, height), common.grid(2 * width, 2 * height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = color
    output[2 * height - r - 1][c] = color
    output[r][2 * width - c - 1] = color
    output[2 * height - r - 1][2 * width - c - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2], cols=[2, 1, 3, 2], color=8),
      generate(rows=[0, 0, 1, 1, 2, 2, 2], cols=[2, 3, 1, 3, 0, 1, 2], color=3),
      generate(rows=[0, 0, 0, 0, 1, 2], cols=[0, 1, 2, 3, 0, 0], color=3),
  ]
  test = [
      generate(rows=[0, 1, 2, 2], cols=[0, 3, 0, 1], color=4),
  ]
  return {"train": train, "test": test}
