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


def generate(col=None, color=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    col: a horizontal coordinate where the pixel should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if col is None:
    col = common.randint(0, size - 1)
    color = common.random_color(exclude=[common.gray()])

  grid, output = common.grids(size, size)
  row = size - 1
  grid[row][col] = color
  while col < size:
    d = -1 if row else 1
    output[row][col] = color
    while row + d >= 0 and row + d < size:
      row += d
      output[row][col] = color
    col += 1
    if col >= size: break
    output[row][col] = common.gray()
    col += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(col=1, color=2),
      generate(col=5, color=3),
      generate(col=4, color=4),
  ]
  test = [
      generate(col=2, color=1),
  ]
  return {"train": train, "test": test}
