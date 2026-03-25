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


def generate(color=None, shape=None):
  """Returns input and output grids according to the given parameters.

  Args:
    color: A color to use.
    shape: A shape to use.
  """

  if color is None:
    color = common.randint(1, 3)
    pixels = common.diagonally_connected_sprite(3, 3, common.randint(1, 5))
    shape = []
    for r in range(3):
      for c in range(3):
        shape.append(1 if (r, c) in pixels else 0)

  grid, output = common.grid(9, 5), common.grid(3, 3)
  grid[1][2] = grid[2][2] = grid[3][2] = 5
  if color == 1: grid[1][1] = grid[1][3] = 5
  if color == 2: grid[1][1] = grid[3][3] = 5
  if color == 3: grid[3][1] = grid[1][3] = 5
  for i, hue in enumerate(shape):
    grid[1 + i // 3][5 + i % 3] = 5 * hue
    output[i // 3][i % 3] = color * hue
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(color=1, shape=[1, 0, 1, 1, 1, 1, 1, 1, 0]),
      generate(color=3, shape=[1, 0, 1, 1, 0, 1, 1, 1, 0]),
      generate(color=1, shape=[1, 0, 1, 0, 1, 1, 1, 0, 1]),
      generate(color=2, shape=[1, 1, 0, 0, 1, 1, 0, 1, 0]),
      generate(color=2, shape=[1, 1, 1, 1, 0, 1, 1, 0, 1]),
      generate(color=2, shape=[1, 0, 0, 0, 1, 1, 1, 0, 0]),
  ]
  test = [
      generate(color=3, shape=[1, 1, 0, 1, 1, 1, 1, 0, 1]),
  ]
  return {"train": train, "test": test}
