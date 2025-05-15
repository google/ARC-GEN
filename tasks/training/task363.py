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


def generate(colors=None, srows=None, scols=None, brows=None,
             bcols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of colors used for the static
    srows: a list of vertical coordinates where sprite data is to be placed
    scols: a list of horizontal coordinates where sprite data is to be placed
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    legal = True
    for r in range(size):
      for c in range(size):
        output[r][c] = grid[r][c] = colors[r * size + c]
    # Draw them black.
    for idx in range(len(brows)):
      brow, bcol = brows[idx], bcols[idx]
      for srow, scol in zip(srows, scols):
        output[brow + srow][bcol + scol] = common.black()
        grid[brow + srow][bcol + scol] = common.black()
    # Check if there are possible locations that we didn't plan (if so, illegal)
    locations = list(zip(brows, bcols))
    for r in range(size):
      for c in range(size):
        possible = True
        for srow, scol in zip(srows, scols):
          if r + srow >= size or c + scol >= size or grid[r + srow][c + scol]:
            possible = False
        if possible and (r, c) not in locations: legal = False
    # Draw them red.
    for idx in range(len(brows)):
      brow, bcol = brows[idx], bcols[idx]
      for srow, scol in zip(srows, scols):
        if output[brow + srow][bcol + scol] == common.red(): legal = False
        output[brow + srow][bcol + scol] = common.red()
        if idx: continue
        grid[brow + srow][bcol + scol] = common.red()
    return legal

  if colors is None:
    while True:
      colors = []
      for _ in range(size * size):
        colors.append(common.gray() if common.randint(0, 2) else common.black())
      wide = common.randint(1, 4)
      tall = 5 - wide
      to_remove = common.randint(0, wide * tall)
      while True:
        srows, scols = common.conway_sprite(wide, tall, to_remove)
        if common.diagonally_connected(list(zip(srows, scols))): break
      num_sprites = common.randint(2, 5)
      brows = [common.randint(0, size - tall) for _ in range(num_sprites)]
      bcols = [common.randint(0, size - wide) for _ in range(num_sprites)]
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 0,
                       5, 0, 5, 5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5,
                       0, 5, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 5, 0,
                       0, 0, 0, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 0, 5, 5,
                       0, 0, 5, 5, 0],
               srows=[0, 1, 1, 2], scols=[1, 0, 2, 1], brows=[0, 1, 5, 6, 7],
               bcols=[5, 7, 6, 0, 5]),
      generate(colors=[0, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 0, 5, 0, 0, 0, 0, 5, 5,
                       5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 5, 5, 0, 5, 5, 5, 0, 0, 0,
                       5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0,
                       0, 5, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 0,
                       5, 5, 5, 5, 5],
               srows=[0, 0, 0, 0], scols=[0, 1, 2, 3], brows=[5, 5],
               bcols=[1, 6]),
      generate(colors=[5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0,
                       5, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0, 0,
                       5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5,
                       0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0,
                       5, 0, 5, 0, 0, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 5],
               srows=[0, 1, 2, 2], scols=[0, 0, 0, 1], brows=[7, 2, 2, 5],
               bcols=[7, 1, 3, 3]),
  ]
  test = [
      generate(colors=[0, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0,
                       5, 0, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 5,
                       5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0,
                       5, 5, 5, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5,
                       5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 0, 5,
                       0, 0, 5, 0, 0],
               srows=[0, 0, 1, 1, 2, 2], scols=[0, 1, 0, 1, 0, 1],
               brows=[4, 2, 7], bcols=[5, 0, 8]),
  ]
  return {"train": train, "test": test}
