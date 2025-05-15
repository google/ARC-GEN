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


def generate(colors=None, cols=None, gravity=None, size=12):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a pair of digits representing two different colors
    cols: a list of horizontal coordinates where centers should be placed
    gravity: which side of the grid is the "bottom" (0: top, 1: left, ...)
    size: the width and height of the (square) grid
  """
  if colors is None:
    colors = common.random_colors(2)
    cols = [common.randint(3, size - 3) for _ in range(2)]
    gravity = common.randint(0, 3)

  grid, output = common.grids(size, size)
  for idx in range(len(cols)):
    r = 2 + 6 * idx
    c = cols[idx]
    output[r][c] = grid[r][c] = colors[0]
    for [dr, dc] in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
      output[r + dr][c + dc] = output[r + 2 * dr][c + 2 * dc] = colors[0]
    for [dr, dc] in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      grid[r + dr][c + dc] = colors[1]
      output[r + dr][c + dc] = output[r + 2 * dr][c + 2 * dc] = colors[1]
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[2, 7], cols=[3, 7], gravity=1),
      generate(colors=[6, 8], cols=[8, 3], gravity=2),
  ]
  test = [
      generate(colors=[4, 3], cols=[7, 2], gravity=1),
  ]
  return {"train": train, "test": test}
