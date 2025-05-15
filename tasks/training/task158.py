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
             megarows=None, megacols=None, mags=None, hflips=None, vflips=None,
             b=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    megarows: a list of vertical coordinates where sprites should be placed
    megacols: a list of horizontal coordinates where 6aa20dc0 should be placed
    mags: a list of sprite magnifiers to be used
    hflips: a list of horizontal flips to be used
    vflips: a list of vertical flips to be used
    b: the integer used for all background cells
  """
  if width is None:
    while True:
      width = common.randint(15, 25)
      height = width + common.randint(-1, 1)
      color_list = common.random_colors(4)
      # First, generate the (diagonally symmetric) sprite.
      rows, cols, colors = [0, 2], [0, 2], [color_list[0], color_list[1]]
      pixels = [(1, 0), (1, 1), (2, 0), (2, 1)]
      pixels = common.sample(pixels, common.randint(2, 3))
      for row, col in pixels:
        rows.append(row)
        cols.append(col)
        colors.append(color_list[2])
        if row == col: continue
        rows.append(col)
        cols.append(row)
        colors.append(color_list[2])
      # Second, place the magnified sprites.
      megarows, megacols, megamags, mags = [], [], [], []
      num_megas = common.randint(2, 4)
      for _ in range(num_megas):
        mag = 1 if not mags else common.randint(1, 3)
        megarow = common.randint(0, height - 3 * mag)
        megacol = common.randint(0, width - 3 * mag)
        if common.overlaps(megarows + [megarow], megacols + [megacol],
                           megamags + [3 * mag], megamags + [3 * mag], 2):
          continue
        megarows.append(megarow)
        megacols.append(megacol)
        megamags.append(3 * mag)
        mags.append(mag)
      if len(mags) == num_megas: break
    hflips = [common.randint(0, 1) for _ in mags]
    vflips = [common.randint(0, 1) for _ in mags]
    # Third, set the background color.
    b = color_list[3]

  grid, output = common.grids(width, height, b)
  for idx, mag in enumerate(mags):
    mrow, mcol, h, v = megarows[idx], megacols[idx], hflips[idx], vflips[idx]
    for row, col, color in zip(rows, cols, colors):
      for dr in range(mag):
        for dc in range(mag):
          r, c = row * mag + dr, col * mag + dc
          r, c = 3 * mag - r - 1 if v else r, 3 * mag - c - 1 if h else c
          output[mrow + r][mcol + c] = color
          if idx > 0 and (row != col or row == 1): continue  # hide pixels
          grid[mrow + r][mcol + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=20, rows=[0, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 1, 0, 2], colors=[2, 8, 8, 8, 8, 8, 3],
               megarows=[4, 1, 11], megacols=[5, 13, 5], mags=[1, 1, 2],
               hflips=[0, 0, 1], vflips=[0, 0, 0], b=1),
      generate(width=21, height=20, rows=[0, 0, 0, 1, 1, 2, 2, 2],
               cols=[0, 1, 2, 0, 2, 0, 1, 2], colors=[6, 1, 1, 1, 1, 1, 1, 2],
               megarows=[2, 7], megacols=[3, 5], mags=[1, 3],
               hflips=[1, 0], vflips=[0, 1], b=4),
      generate(width=22, height=21, rows=[0, 0, 1, 1, 1, 2, 2],
               cols=[0, 1, 0, 1, 2, 1, 2], colors=[2, 3, 3, 3, 3, 3, 4],
               megarows=[5, 10, 14], megacols=[6, 13, 5], mags=[1, 1, 1],
               hflips=[0, 1, 1], vflips=[0, 1, 0], b=8),
  ]
  test = [
      generate(width=22, height=22, rows=[0, 0, 1, 1, 2, 2],
               cols=[0, 1, 0, 2, 1, 2], colors=[4, 8, 8, 8, 8, 1],
               megarows=[4, 1, 13, 13], megacols=[5, 10, 1, 11],
               mags=[1, 3, 1, 2], hflips=[1, 0, 1, 0], vflips=[0, 0, 1, 1],
               b=3),
  ]
  return {"train": train, "test": test}
