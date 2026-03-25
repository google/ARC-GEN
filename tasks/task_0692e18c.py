# Copyright 2026 Google LLC
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


def generate(rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the input pixels.
    cols: The columns of the input pixels.
    color: The color of the input pixels.
  """

  if color is None:
    color = common.random_color()
    rows, cols = common.conway_sprite(3, 3)

  grid, output = common.grid(3, 3), common.grid(9, 9)
  for row, col in zip(rows, cols):
    grid[row][col] = color
    for r in range(3):
      for c in range(3):
        output[3 * row + r][3 * col + c] = color
    for r, c in zip(rows, cols):
      output[3 * row + r][3 * col + c] = 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2], cols=[2, 1, 0], color=6),
      generate(rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], color=7),
      generate(rows=[0, 0, 1, 2], cols=[0, 1, 2, 2], color=4),
  ]
  test = [
      generate(rows=[0, 1, 1, 2], cols=[2, 0, 1, 1], color=3),
  ]
  return {"train": train, "test": test}
