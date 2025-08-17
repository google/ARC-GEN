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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             megarows=None, megacols=None, megarotates=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    megarows: a list of vertical coordinates for sprite placement
    megacols: a list of horizontal coordinates for sprite placement
    megarotates: a list of digits representing the rotations of mega-sprites
  """
  if width is None:
    width, height = common.randint(13, 15), common.randint(13, 15)
    # Choose the dimensions of the rainbow sprites.
    sprite_type, wide, tall = common.randint(0, 2), 3, 3
    if sprite_type == 1: wide, tall = 4, 2
    if sprite_type == 2: wide, tall = 5, 1
    # Choose the positions of the yellow pixels.
    while True:
      pixels = common.sample(common.all_pixels(wide, tall), 5)
      if common.diagonally_connected(pixels): break
    extra_pixels, colors, extra_colors = [], [4] * len(pixels), []
    # Choose the number of pixels of each other color.
    num_red, num_blue, num_green = 1, common.randint(1, 2), common.randint(1, 3)
    extra_colors += [common.red()] * num_red
    extra_colors += [common.blue()] * num_blue
    extra_colors += [common.green()] * num_green
    # Choose the positions of the other pixels (make sure they don't clobber).
    for color in extra_colors:
      while True:
        pixel, angle = common.choice(pixels), common.randint(0, 3)
        r, c = pixel[0], pixel[1]
        if angle == 0: r -= 1
        if angle == 1: r += 1
        if angle == 2: c -= 1
        if angle == 3: c += 1
        # The red pixel is important; don't place it in the center.
        if color == common.red() and (r == tall // 2 or c == wide // 2):
          continue
        if (r, c) not in pixels and (r, c) not in extra_pixels: break
      extra_pixels.append((r, c))
    # Add the extra pixels & colors, and shift the row/col values if needed.
    colors, pixels = colors + extra_colors, pixels + extra_pixels
    rows, cols = zip(*pixels)
    rows, cols = [r - min(rows) for r in rows], [c - min(cols) for c in cols]
    wide, tall = max(cols) + 1, max(rows) + 1
    # Choose the positions of the mega-sprites, making sure they don't overlap.
    num_sprites = common.randint(3, 4)
    megarotates = [common.randint(0, 3) for _ in range(num_sprites)]
    while True:
      megarows, megacols, megawides, megatalls = [], [], [], []
      for megarotate in megarotates:
        w, t = (tall, wide) if megarotate == 1 else (wide, tall)
        megarows.append(common.randint(0, height - t))
        megacols.append(common.randint(0, width - w))
        megawides.append(w)
        megatalls.append(t)
      if not common.overlaps(megarows, megacols, megawides, megatalls, 1): break

  grid, output = common.grids(width, height)
  wide, tall = max(cols) + 1, max(rows) + 1
  for i, megarotate in enumerate(megarotates):
    mr, mc = megarows[i], megacols[i]
    for row, col, color in zip(rows, cols, colors):
      r, c = row, col
      if megarotate == 1: r, c = c, tall - 1 - r
      if megarotate == 2: r, c = tall - 1 - r, wide - 1 - c
      if megarotate == 3: c = wide - 1 - c
      output[mr + r][mc + c] = color
      if i != 0 and color not in [common.yellow(), common.red()]: continue
      grid[mr + r][mc + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13, rows=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               cols=[1, 3, 4, 0, 1, 2, 3, 4, 0, 2, 4],
               colors=[1, 1, 2, 4, 4, 4, 4, 4, 3, 3, 3], megarows=[1, 2, 7],
               megacols=[1, 9, 3], megarotates=[0, 1, 2]),
      generate(width=13, height=13, rows=[0, 1, 1, 1, 1, 2, 3, 3, 3, 3],
               cols=[2, 0, 1, 2, 3, 2, 0, 1, 2, 3],
               colors=[2, 4, 4, 4, 1, 4, 3, 3, 4, 3], megarows=[1, 4, 9],
               megacols=[2, 8, 3], megarotates=[0, 3, 1]),
      generate(width=13, height=13, rows=[0, 0, 1, 1, 1, 1, 2, 2, 3],
               cols=[2, 3, 0, 1, 2, 3, 1, 2, 2],
               colors=[4, 2, 1, 4, 4, 4, 3, 4, 1], megarows=[1, 5, 8],
               megacols=[1, 7, 3], megarotates=[0, 3, 2]),
  ]
  test = [
      generate(width=15, height=14, rows=[0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
               cols=[0, 1, 0, 1, 2, 0, 2, 3, 1, 2, 3],
               colors=[1, 3, 4, 4, 2, 4, 4, 3, 4, 4, 1], megarows=[2, 3, 9, 8],
               megacols=[2, 10, 0, 7], megarotates=[0, 1, 2, 3]),
  ]
  return {"train": train, "test": test}
