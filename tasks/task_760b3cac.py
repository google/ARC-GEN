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


def generate(rows=None, cols=None, flip=None, width=9, height=6):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    flip: whether to flip the grid
    width: the width of the grid
    height: the height of the grid
  """
  if rows is None:
    while True:
      rows, cols = common.conway_sprite()
      # Make sure it looks sufficiently different than the yellow sprite
      if len(rows) == 5 and common.connected(list(zip(rows, cols))): continue
      break
    flip = common.randint(0, 1)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][2 - c] = output[r][c + 3] = grid[r][c + 3] = common.cyan()
  for r, c in [(3, 3), (4, 3), (4, 4), (4, 5), (5, 4)]:
    output[r][c] = grid[r][c] = common.yellow()
  if flip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 1, 2, 2], flip=0),
      generate(rows=[0, 0, 1, 1, 1, 2, 2], cols=[0, 2, 0, 1, 2, 1, 2], flip=1),
      generate(rows=[0, 1, 1, 2], cols=[0, 1, 2, 0], flip=0),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2], cols=[0, 2, 0, 1, 2], flip=1),
  ]
  return {"train": train, "test": test}
