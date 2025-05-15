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


def generate(rows=None, cols=None, srow=None, scol=None, rdirs=None, cdirs=None,
             colors=None, size=21):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    srow: the vertical coordinate of the middle sprite
    scol: the horizontal coordinate of the middle sprite
    rdirs: a list of vertical directions to stamp the sprite
    cdirs: a list of horizontal directions to stamp the sprite
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    # First, choose a sprite.
    sprite, rows, cols = [[1, 1, 1], [1, 1, 1], [1, 1, 1]], [], []
    rbad, cbad = 0, 0  # A direction to be avoided.
    if common.randint(0, 1): sprite[1][1] = 0  # Remove the middle pixel
    if common.randint(0, 1):  # Remove one side cell
      side = common.randint(0, 3)
      if side == 0: sprite[0][1], rbad, cbad = 0, 1, 0
      if side == 1: sprite[1][2], rbad, cbad = 0, 0, -1
      if side == 2: sprite[2][1], rbad, cbad = 0, -1, 0
      if side == 3: sprite[1][0], rbad, cbad = 0, 0, 1
    else:  # If we didn't remove a side, maybe remove some (or both) diagonals
      if common.randint(0, 1): sprite[0][0] = sprite[2][2] = 0
      if common.randint(0, 1): sprite[0][2] = sprite[2][0] = 0
    for r in range(3):
      for c in range(3):
        if sprite[r][c]: rows, cols = rows + [r], cols + [c]
    # Second, choose a placement for the middle sprite.
    srow, scol = common.randint(6, size - 9), common.randint(6, size - 9)
    # Third, sample two or three directions to stamp the sprite.
    dirs = []
    for rdir in [-1, 0, 1]:
      for cdir in [-1, 0, 1]:
        if rdir == 0 and cdir == 0: continue
        if rdir == rbad and cdir == cbad: continue
        dirs.append((rdir, cdir))
    dirs = [(0, 0)] + common.sample(dirs, common.randint(2, 3))
    rdirs, cdirs = zip(*dirs)
    color = common.random_color()  # We'll pick a special color for the middle.
    colors = [color] + [common.random_color(exclude=[color]) for _ in dirs]

  grid, output = common.grids(size, size)
  def put(thegrid, r, c, thecolor):
    if r >= 0 and r < size and c >= 0 and c < size:
      thegrid[r][c] = thecolor
  for rdir, cdir, color in zip(rdirs, cdirs, colors):
    middle_sprite, first_sprite = (rdir == 0 and cdir == 0), True
    row, col = srow, scol
    while True:
      row, col = row + 4 * rdir, col + 4 * cdir
      for (r, c) in zip(rows, cols):
        put(output, row + r, col + c, color)
        if middle_sprite:
          put(grid, row + r, col + c, color)
        if first_sprite and r * rdir + 1 - rdir + c * cdir + 1 - cdir < 2:
          put(grid, row + r, col + c, color)
      first_sprite = False
      if middle_sprite: break  # It's the middle sprite
      if row < -5 or row > size or col < -5 or col > size: break
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2], cols=[0, 1, 2, 0, 2, 0, 1, 2],
               srow=6, scol=6, rdirs=[0, 1, 0], cdirs=[0, 0, 1],
               colors=[8, 2, 3]),
      generate(rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], srow=7, scol=11,
               rdirs=[0, 0, -1, 0], cdirs=[0, -1, 0, 1], colors=[1, 2, 4, 4]),
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[0, 1, 0, 2, 1, 2], srow=7, scol=6,
               rdirs=[0, -1, 1], cdirs=[0, 1, 1], colors=[5, 6, 1]),
  ]
  test = [
      generate(rows=[0, 0, 0, 1, 1, 2, 2], cols=[0, 1, 2, 0, 2, 0, 2], srow=7,
               scol=6, rdirs=[0, -1, 0, 1], cdirs=[0, 1, 1, 0],
               colors=[8, 4, 2, 3]),
  ]
  return {"train": train, "test": test}
