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


def generate(rows=None, cols=None, color=None, width=2, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    width: the width the input grid
    height: the height the input grid
  """
  if rows is None:
    while True:
      pixels = common.random_pixels(width, height)
      if pixels: break
    rows, cols = zip(*pixels)
    color = common.random_color()

  grid = common.grid(width, height)
  output = common.grid(2 * width, 3 * height)
  for r, c in zip(rows, cols):
    grid[r][c] = color
    output[height - 1 - r][width + c] = color
    output[height - 1 - r][width - 1 - c] = color
    output[height + r][width + c] = color
    output[height + r][width - 1 - c] = color
    output[3 * height - 1 - r][width + c] = color
    output[3 * height - 1 - r][width - 1 - c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 2], cols=[1, 1], color=8),
      generate(rows=[0, 1, 1, 2], cols=[0, 0, 1, 0], color=2),
      generate(rows=[1, 2], cols=[1, 0], color=5),
  ]
  test = [
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 1, 0, 0, 1], color=3),
  ]
  return {"train": train, "test": test}
