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


def generate(width=None, height=None, depth=None, row=None, col=None,
             colors=None, gravity=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of one grid half
    height: the height of the grid
    depth: how deep the laser is
    row: a vertical coordinate where the laser should be placed
    col: a horizontal coordinate where the laser should be placed
    colors: the colors of the laser and its beam
    gravity: which direction the laser should be oriented
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    depth = common.randint(3, 4)
    row = common.randint(1, height - depth - 1)
    col = common.randint(depth, width - depth - 1)
    colors = common.random_colors(2)
    gravity = common.randint(0, 3)

  grid, output = common.grids(width, height)
  for d in range(depth):
    for dc in range(d - depth + 1, depth - d):
      output[row + d][col + dc] = grid[row + d][col + dc] = colors[0]
  output[row][col] = grid[row][col] = colors[1]
  for r in range(row + depth, height):
    output[r][col] = colors[1]
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=15, depth=3, row=3, col=4, colors=[2, 1],
               gravity=1),
      generate(width=12, height=12, depth=4, row=3, col=6, colors=[8, 3],
               gravity=2),
      generate(width=12, height=15, depth=3, row=2, col=4, colors=[3, 2],
               gravity=0),
  ]
  test = [
      generate(width=11, height=16, depth=4, row=1, col=4, colors=[4, 8],
               gravity=2),
  ]
  return {"train": train, "test": test}
