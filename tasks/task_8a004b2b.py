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
             shows=None, wide=None, tall=None, brow=None, bcol=None, irow=None,
             icol=None, srow=None, scol=None, mag=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of colors to be used for the pixels
    shows: a subset of pixel indices to show magnified
    wide: the width of the yellow box
    tall: the height of the yellow box
    brow: a vertical coordinate where the box should be placed
    bcol: a horizontal coordinate where the box should be placed
    irow: a vertical coordinate inside the box where the sprite should be
    icol: a horizontal coordinate inside the box where the sprite should be
    srow: a vertical coordinate where the full sprite should be
    scol: a horizontal coordinate where the full sprite should be
    mag: the magnification factor
  """
  if width is None:
    width, height = common.randint(15, 20), common.randint(15, 20)
    mag = common.randint(2, min(4, (height + 1) // 5))
    w, t = common.randint(2, 7 - mag), common.randint(2, 3)
    num_pixels = common.randint(max(4, w * t // 2), w * t)
    pixels = common.continuous_creature(num_pixels, w, t)
    rows, cols = zip(*pixels)
    colors = [common.choice([1, 2, 3, 8]) for _ in pixels]
    num_show = common.randint(2, num_pixels // 2)
    shows = common.sample(range(len(pixels)), num_show)
    wide = common.randint(mag * w + 2, width)
    tall = common.randint(mag * t + 2, height - 4)
    brow = common.randint(0, height - 4 - tall)
    bcol = common.randint(0, width - wide)
    irow = common.randint(1, tall - 1 - mag * t)
    icol = common.randint(1, wide - 1 - mag * w)
    srow = height - t - 1
    scol = common.randint(1, width - 1 - w)

  grid, output = common.grid(width, height), common.grid(wide, tall)
  for r, c in [(0, 0), (0, wide - 1), (tall - 1, 0), (tall - 1, wide - 1)]:
    grid[brow + r][bcol + c] = common.yellow()
    output[r][c] = common.yellow()
  for idx, color in enumerate(colors):
    row, col = rows[idx], cols[idx]
    grid[srow + row][scol + col] = color
    for dr in range(mag):
      for dc in range(mag):
        r, c = irow + row * mag + dr, icol + col * mag + dc
        if idx in shows: grid[brow + r][bcol + c] = color
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=17,
               rows=[0, 0, 1, 1, 1, 1, 2, 2, 2],
               cols=[0, 4, 0, 1, 3, 4, 1, 2, 3],
               colors=[3, 2, 1, 1, 1, 1, 1, 1, 1],
               shows=[0, 1, 7], wide=14, tall=9,
               brow=0, bcol=2, irow=2, icol=1, srow=12, scol=2, mag=2),
      generate(width=18, height=17,
               rows=[0, 0, 1, 1],
               cols=[0, 1, 0, 1],
               colors=[2, 3, 3, 8],
               shows=[0, 3], wide=7, tall=7,
               brow=1, bcol=2, irow=1, icol=1, srow=13, scol=10, mag=2),
      generate(width=18, height=16,
               rows=[0, 0, 0, 1, 1],
               cols=[0, 1, 2, 1, 2],
               colors=[2, 1, 1, 3, 1],
               shows=[0, 2, 3], wide=11, tall=11,
               brow=0, bcol=3, irow=3, icol=1, srow=13, scol=6, mag=3),
  ]
  test = [
      generate(width=18, height=19,
               rows=[0, 0, 1, 1, 1, 2],
               cols=[0, 2, 0, 1, 2, 1],
               colors=[8, 3, 1, 1, 1, 1],
               shows=[0, 1], wide=18, tall=14,
               brow=0, bcol=0, irow=2, icol=4, srow=15, scol=8, mag=4),
  ]
  return {"train": train, "test": test}
