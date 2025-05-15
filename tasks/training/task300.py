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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices of the sprites
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    num_sprites = max(3, common.randint(1, 4))
    while True:
      height = common.randint(5, 9)
      width = common.randint(9, 20 - height)
      sizes = sorted(common.sample(range(3, 10), num_sprites), reverse=True)
      # Adjust the sprite bounding box based on its size.
      wides, talls = [], []
      for size in sizes:
        wide, tall = 2, 2
        if size >= 4: wide = 3
        if size >= 6: tall = 3
        if size >= 9: tall = 4
        wides.append(wide)
        talls.append(tall)
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    # Now, settle on the content of the sprites (it doesn't matter much).
    rows, cols, idxs = [], [], []
    for idx in range(num_sprites):
      wide, tall, size = wides[idx], talls[idx], sizes[idx]
      pixels = common.continuous_creature(size, wide, tall)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))
    colors = common.random_colors(num_sprites)

  wide = max([c for c, i in zip(cols, idxs) if not i]) + 1
  tall = max([r for r, i in zip(rows, idxs) if not i]) + 1
  grid, output = common.grid(width, height), common.grid(wide, tall)
  for r, c, idx in zip(rows, cols, idxs):
    grid[r + brows[idx]][c + bcols[idx]] = colors[idx]
    if not idx: output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=7,
               rows=[0, 0, 1, 2, 2, 3, 3, 3, 0, 0, 1, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 1, 1, 2, 0, 1, 2, 0, 1, 1, 1, 0, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2],
               brows=[1, 1, 2], bcols=[1, 5, 8], colors=[2, 3, 1]),
      generate(width=10, height=5,
               rows=[0, 0, 1, 1, 2, 2, 0, 1, 1, 1, 2, 0, 0, 1],
               cols=[0, 1, 0, 1, 0, 1, 1, 0, 1, 2, 1, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
               brows=[1, 1, 0], bcols=[4, 0, 7], colors=[4, 3, 6]),
      generate(width=11, height=6,
               rows=[0, 0, 0, 1, 2, 2, 3, 3, 0, 0, 1, 2, 3, 0, 1, 1, 2],
               cols=[0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 1, 2], bcols=[1, 8, 5], colors=[8, 7, 2]),
      generate(width=9, height=7,
               rows=[0, 0, 0, 1, 2, 2, 2, 0, 1, 1, 2, 0, 0, 0, 1],
               cols=[0, 1, 2, 1, 0, 1, 2, 0, 0, 1, 1, 0, 1, 2, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 1, 4], bcols=[6, 3, 0], colors=[2, 7, 8]),
  ]
  test = [
      generate(width=9, height=9,
               rows=[0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0,
                     1, 1, 0, 1, 1, 2],
               cols=[0, 1, 2, 0, 1, 2, 0, 2, 0, 2, 1, 2, 0, 1, 2, 0, 1, 0, 1, 2,
                     0, 1, 0, 0, 1, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
                     2, 2, 3, 3, 3, 3],
               brows=[2, 6, 7, 1], bcols=[3, 6, 1, 0], colors=[3, 6, 5, 4]),
  ]
  return {"train": train, "test": test}
