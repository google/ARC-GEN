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


def generate(size=None, row=None, col=None, spacing=None, flip=None,
             color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the size of the (square) grid
    row: a vertical coordinate for the middle pixel
    col: a horizontal coordinates for the middle pixel
    spacing: the distance between the middle pixel and its neighbors
    flip: whether to flip the pixels
    color: the integer used for all pixels
  """
  if size is None:
    size = common.randint(20, 30)
    spacing = common.randint(2, size // 4)
    row = common.randint(spacing, size - spacing - 1)
    col = common.randint(spacing, size - spacing - 1)
    flip, color = common.randint(0, 1), common.random_color()

  grid, output = common.grids(size, size)
  output[row][col] = grid[row][col] = color
  grid[row - spacing][col + spacing if flip else col - spacing] = color
  grid[row + spacing][col - spacing if flip else col + spacing] = color
  s = spacing
  while True:
    if row - s < 0 and row + s >= size and col - s < 0 and col + s >= size:
      break
    for i in range(-s, s + 1):
      common.draw(output, row - s, col + i, color)
      common.draw(output, row + s, col + i, color)
      common.draw(output, row + i, col + s, color)
      common.draw(output, row + i, col - s, color)
    s += spacing
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=23, row=5, col=14, spacing=3, flip=0, color=8),
      generate(size=23, row=13, col=11, spacing=2, flip=1, color=2),
      generate(size=23, row=8, col=8, spacing=4, flip=1, color=3),
  ]
  test = [
      generate(size=28, row=18, col=13, spacing=6, flip=0, color=4),
  ]
  return {"train": train, "test": test}
