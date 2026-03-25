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


def generate(width=None, height=None, wide=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wide: The width of the sprite.
    colors: The colors of the sprite.
  """

  if width is None:
    width, height = 2 * common.randint(4, 7), common.randint(3, 4)
    wide = common.randint(3, 4)
    colors = common.choices([1, 2, 3, 8], wide * height)
    for r in range(height):
      colors[r * wide + wide - 1] = colors[r * wide]

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      output[r][c] = colors[r * wide]
  for i, color in enumerate(colors):
    output[i // wide][i % wide] = grid[i // wide][i % wide] = color
    output[i // wide][width - wide + i % wide] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=4, wide=3,
               colors=[3, 2, 3, 1, 2, 1, 3, 2, 3, 1, 3, 1]),
      generate(width=10, height=3, wide=3,
               colors=[8, 2, 8, 1, 8, 1, 1, 8, 1]),
      generate(width=14, height=3, wide=4,
               colors=[2, 3, 8, 2, 2, 8, 8, 2, 2, 8, 3, 2]),
  ]
  test = [
      generate(width=14, height=4, wide=4,
               colors=[3, 8, 8, 3, 2, 1, 1, 2, 1, 3, 3, 1, 2, 1, 1, 2]),
  ]
  return {"train": train, "test": test}
