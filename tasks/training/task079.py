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


def generate(rows=None, cols=None, idxs=None, megarows=None, megacols=None,
             megaidxs=None, colors=None, size=14):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of sprite indices
    megarows: a list of vertical coordinates where sprites should be placed
    megacols: a list of horizontal coordinates where sprites should be placed
    megaidxs: a list of sprite indices for each sprite
    colors: a list of colors to be used for each sprite type
    size: the width and height of the (square) grid
  """
  if rows is None:
    # First chose 2 or 3 sprites along with their colors.
    colors = common.random_colors(common.randint(2, 3))
    sprite_types = []
    while len(sprite_types) < len(colors):
      while True:
        rows, cols = common.conway_sprite()
        if common.diagonally_connected(list(zip(rows, cols))): break
      sprite = list(zip(rows, cols))
      sprite.sort()
      if sprite not in sprite_types: sprite_types.append(sprite)
    rows, cols, idxs = [], [], []
    for idx, sprite in enumerate(sprite_types):
      rows.extend([s[0] for s in sprite])
      cols.extend([s[1] for s in sprite])
      idxs.extend([idx] * len(sprite))
    # Next, choose how many copies of each sprite type to place.
    num_sprites_per_type = common.sample(range(1, 4), len(colors))
    num_sprites_per_type.sort(reverse=True)
    # Finally, pick some non-overlapping locations for all the sprites.
    while True:
      megarows, megacols, megaidxs = [], [], []
      for idx, num in enumerate(num_sprites_per_type):
        megarows.extend([common.randint(0, size - 3) for _ in range(num)])
        megacols.extend([common.randint(0, size - 3) for _ in range(num)])
        megaidxs.extend([idx] * num)
      lengths = [3] * len(idxs)
      if not common.overlaps(megarows, megacols, lengths, lengths, 1): break

  grid, output = common.grid(size, size), common.grid(3, 3)
  for megarow, megacol, megaidx in zip(megarows, megacols, megaidxs):
    for row, col, idx in zip(rows, cols, idxs):
      if idx != megaidx: continue
      grid[megarow + row][megacol + col] = colors[megaidx]
      output[row][col] = output[row][col] if idx != 0 else colors[megaidx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2, 2, 0, 0, 1, 1, 2],
               cols=[0, 2, 1, 0, 2, 0, 2, 0, 2, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               megarows=[1, 2, 7, 7, 11], megacols=[2, 10, 3, 9, 1],
               megaidxs=[0, 0, 0, 1, 1], colors=[8, 2]),
      generate(rows=[0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 0, 0, 1, 2, 2],
               cols=[0, 1, 2, 0, 0, 2, 0, 1, 2, 1, 0, 2, 1, 0, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               megarows=[0, 1, 3, 5, 6, 8, 10, 11],
               megacols=[7, 2, 11, 6, 1, 9, 2, 11],
               megaidxs=[1, 0, 0, 2, 1, 0, 0, 1], colors=[4, 1, 2]),
      generate(rows=[0, 1, 1, 1, 2, 0, 0, 1, 1, 2],
               cols=[1, 0, 1, 2, 1, 0, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               megarows=[2, 2, 8], megacols=[2, 9, 8], megaidxs=[0, 1, 0],
               colors=[8, 6]),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[1, 0, 1, 2, 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               megarows=[2, 2, 7, 8, 11, 11], megacols=[3, 9, 6, 0, 4, 9],
               megaidxs=[1, 0, 2, 0, 0, 1], colors=[2, 3, 8]),
  ]
  return {"train": train, "test": test}
