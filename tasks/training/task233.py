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

import sys

import common


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             srows=None, scols=None, colors=None, irows=None, icols=None,
             rotates=None, wide=None, tall=None, brow=None, bcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprites list
    srows: a list of vertical coordinates where the sprites should be placed
    scols: a list of horizontal coordinates where the sprites should be placed
    colors: a list of colors to be used for the sprites
    irows: a list of vertical coordinates insides the red box
    icols: a list of horizontal coordinates insides the red box
    rotates: a list of rotations to be applied to the sprites
    wide: the width of the output grid
    tall: the height of the output grid
    brow: the vertical coordinate of the top left corner of the red box
    bcol: the horizontal coordinate of the top left corner of the red box
  """

  def draw(grid, output):
    # Draw the big red boxes.
    for r in range(tall):
      for c in range(wide):
        output[r][c] = grid[r + brow][c + bcol] = common.red()
    # Draw the sprite background colors (outside for input, inside for output)
    for idx, color in enumerate(colors):
      for dr in range(3):
        for dc in range(3):
          grid[srows[idx] + dr][scols[idx] + dc] = color
          output[irows[idx] + dr][icols[idx] + dc] = color
    # Draw sprites (black inside + red outside for input, red inside for output)
    # Along the way, check that we're not touching edges of another sprite.
    illegal = False
    for sprite_idx in set(idxs):
      for row, col, idx in zip(rows, cols, idxs):
        if idx != sprite_idx: continue
        r, c = row, col
        if rotates[idx] == 1: r, c = c, 2 - r
        if rotates[idx] == 2: r, c = 2 - r, 2 - c
        if rotates[idx] == 3: r, c = 2 - c, r
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            v = grid[brow + irows[idx] + r + dr][bcol + icols[idx] + c + dc]
            if v == common.black(): illegal = True
      for row, col, idx in zip(rows, cols, idxs):
        if idx != sprite_idx: continue
        r, c = row, col
        if rotates[idx] == 1: r, c = c, 2 - r
        if rotates[idx] == 2: r, c = 2 - r, 2 - c
        if rotates[idx] == 3: r, c = 2 - c, r
        grid[srows[idx] + row][scols[idx] + col] = common.red()
        grid[brow + irows[idx] + r][bcol + icols[idx] + c] = common.black()
        output[irows[idx] + r][icols[idx] + c] = common.red()
    return not illegal

  if width is None:
    num_sprites = common.randint(1, 5)
    # Choose positions until everything fits and nothing overlaps.
    while True:
      wide, tall = common.randint(8, 20), common.randint(8, 20)
      width, height = wide + common.randint(2, 10), tall + common.randint(2, 10)
      brow = common.randint(1, height - tall - 1)
      bcol = common.randint(1, width - wide - 1)
      srows = [common.randint(0, height - 3) for _ in range(num_sprites)]
      scols = [common.randint(0, width - 3) for _ in range(num_sprites)]
      irows = [common.randint(1, tall - 4) for _ in range(num_sprites)]
      icols = [common.randint(1, wide - 4) for _ in range(num_sprites)]
      lens = [3] * num_sprites
      if common.overlaps(srows + [brow], scols + [bcol], lens + [wide],
                         lens + [tall], 1): continue
      if common.overlaps(irows, icols, lens, lens, 0): continue
      counts = common.sample(range(4, 9), num_sprites)
      rows, cols, idxs = [], [], []
      for idx in range(num_sprites):
        while True:  # Avoid sprites where rotation might be ambiguous.
          pixels = common.sample(common.all_pixels(3, 3), counts[idx])
          num_blank = 0
          for r in range(3):
            blank = True
            for c in range(3):
              if (r, c) in pixels: blank = False
            if blank: num_blank += 1
          for c in range(3):
            blank = True
            for r in range(3):
              if (r, c) in pixels: blank = False
            if blank: num_blank += 1
          if counts[idx] == 4 and num_blank >= 2: continue  # Avoid 2x2
          if counts[idx] == 6 and num_blank >= 1: continue  # Avoid 2x3
          break
        rows.extend(p[0] for p in pixels)
        cols.extend(p[1] for p in pixels)
        idxs.extend([idx] * len(pixels))
      rotates = [0] * num_sprites
      colors = common.random_colors(num_sprites, exclude=[common.red()])
      grid, output = common.grid(width, height), common.grid(wide, tall)
      if draw(grid, output): break

  grid, output = common.grid(width, height), common.grid(wide, tall)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=24,
               rows=[0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 0, 1, 1, 1,
                     2],
               cols=[1, 0, 1, 2, 1, 0, 1, 2, 0, 2, 0, 1, 2, 1, 0, 1, 2, 0, 1, 2,
                     2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4,
                     4],
               srows=[2, 7, 17, 20, 20], scols=[13, 14, 14, 3, 8],
               irows=[6, 1, 13, 1, 13], icols=[3, 6, 0, 1, 5],
               rotates=[0, 1, 3, 1, 1], colors=[1, 3, 8, 4, 5], wide=9, tall=17,
               brow=1, bcol=2),
      generate(width=10, height=20,
               rows=[0, 1, 1, 2, 0, 0, 1, 1, 2, 2],
               cols=[1, 0, 1, 1, 0, 1, 0, 2, 1, 2],
               idxs=[0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               srows=[11, 13], scols=[1, 5], irows=[1, 4], icols=[1, 4],
               rotates=[1, 0], colors=[4, 3], wide=8, tall=8, brow=1, bcol=1),
      generate(width=12, height=16,
               rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1], idxs=[0, 0, 0, 0, 0],
               srows=[1], scols=[5], irows=[2], icols=[2], rotates=[0],
               colors=[8], wide=9, tall=9, brow=6, bcol=1),
  ]
  test = [
      generate(width=15, height=19,
               rows=[1, 0, 1, 1, 2, 0, 1, 1, 2, 2, 0, 1, 2],
               cols=[1, 0, 0, 1, 0, 2, 1, 2, 0, 1, 1, 1, 1],
               idxs=[0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3],
               srows=[11, 11, 15, 16], scols=[1, 8, 11, 3], irows=[0, 1, 1, 5],
               icols=[9, 4, 1, 7], rotates=[0, 2, 1, 1], colors=[1, 3, 8, 4],
               wide=12, tall=8, brow=1, bcol=2),
  ]
  return {"train": train, "test": test}
