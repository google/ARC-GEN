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


def generate(width=None, height=None, rows=None, cols=None, brows=None,
             bcols=None, bmags=None, colors=None, shows=None, pcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    bmags: a list of sprite magnifiers
    colors: a list of colors to be used for the sprites
    shows: a list of indices of the pixel to be shown for each sprite
    pcolor: a color to be used for the "signature" pixel
  """
  if width is None:
    num_sprites = common.randint(2, 4)
    wide, tall = 3, 3
    # First, choose grid dimensions and sprite magnifiers / locations.
    while True:
      width, height = common.randint(10, 30), common.randint(10, 30)
      bmags = [common.randint(1, 4) for _ in range(num_sprites)]
      bmags[0] = 1  # The first one should have no magnifier.
      wides = [bmag * wide for bmag in bmags]
      talls = [bmag * tall for bmag in bmags]
      if max(wides) > width or max(talls) > height: continue  # Too big.
      brows = [common.randint(0, height - t) for t in talls]
      bcols = [common.randint(0, width - w) for w in wides]
      if not common.overlaps(brows, bcols, wides, talls, 2): break
    # Second, choose sprite contents.
    num_pixels = wide * tall // 2 + common.randint(-1, 1)
    pixels = common.continuous_creature(num_pixels, wide, tall)
    rows, cols = zip(*pixels)
    while True:  # Make sure we show pixels that are adjacent to the first pixel
      shows = [common.randint(1, len(pixels) - 1) for _ in range(num_sprites)]
      all_adjacent = True
      for s in shows:
        d = abs(pixels[0][0] - pixels[s][0]) + abs(pixels[0][1] - pixels[s][1])
        if d > 1: all_adjacent = False
      if all_adjacent: break
    pcolor = common.random_color()
    colors = common.random_colors(num_sprites, exclude=[pcolor])

  grid, output = common.grids(width, height)
  for idx, bmag in enumerate(bmags):
    brow, bcol, color, show = brows[idx], bcols[idx], colors[idx], shows[idx]
    for i in range(len(rows)):
      row, col = rows[i], cols[i]
      for dr in range(bmag):
        for dc in range(bmag):
          r, c = brow + row * bmag + dr, bcol + col * bmag + dc
          common.draw(output, r, c, color if i else pcolor)
          if idx and i not in [0, show]: continue  # Usually draw just 2 pixels.
          common.draw(grid, r, c, color if i else pcolor)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=16, rows=[1, 1, 1, 0, 2], cols=[2, 1, 0, 1, 1],
               brows=[1, 7], bcols=[2, 3], bmags=[1, 2], colors=[3, 4],
               shows=[0, 1], pcolor=1),
      generate(width=18, height=16, rows=[1, 1, 1, 1, 0, 2],
               cols=[0, 1, 2, 3, 3, 3], brows=[1, 6, 11], bcols=[2, 10, 5],
               bmags=[1, 1, 1], colors=[8, 6, 3], shows=[0, 1, 1], pcolor=2),
      generate(width=18, height=17, rows=[1, 0, 2, 1, 0, 2, 1, 0],
               cols=[1, 1, 0, 0, 0, 2, 2, 2], brows=[2, 7], bcols=[2, 6],
               bmags=[1, 3], colors=[1, 8], shows=[0, 1], pcolor=4),
      generate(width=18, height=15, rows=[1, 1, 1, 0, 2], cols=[2, 1, 0, 2, 2],
               brows=[3, 1, 7], bcols=[12, 3, 2], bmags=[1, 1, 2],
               colors=[8, 3, 4], shows=[0, 1, 3], pcolor=2),
  ]
  test = [
      generate(width=30, height=19, rows=[1, 1, 1, 0, 0, 2, 2],
               cols=[1, 0, 2, 1, 2, 0, 1], brows=[2, 0, 3, 8],
               bcols=[3, 10, 17, 4], bmags=[1, 3, 4, 2], colors=[8, 4, 2, 3],
               shows=[0, 1, 2, 6], pcolor=1),
  ]
  return {"train": train, "test": test}
