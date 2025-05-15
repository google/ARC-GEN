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


def generate(width=None, height=None, linecols=None, linecolors=None,
             rows=None, cols=None, colors=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    linecols: a list of horizontal coordinates where lines should be placed
    linecolors: a list of digits representing colors to be used for the lines
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used for the pixels
    xpose: whether to transpose the input grid
  """
  if width is None:
    width, height = common.randint(12, 30), common.randint(12, 30)
    # Choose the line locations and colors (plus an "extra" color).
    c, linecols = common.randint(3, 6), []
    while c < width:
      linecols.append(c)
      c += common.randint(6, 9)
    linecolors = common.random_colors(len(linecols) + 1)
    # Choose the pixels locations and colors.
    pixels = common.random_pixels(width, height, 0.02)
    color_idxs = [common.randint(0, len(linecolors) - 1) for _ in pixels]
    # Remove pixels that fall on (or close to) a line, or are on the same row as
    # a same color.
    rows, cols, colors = [], [], []
    for color in linecolors:
      rows_taken = []
      for i, pixel in enumerate(pixels):
        if linecolors[color_idxs[i]] != color: continue
        if pixel[0] in rows_taken or pixel[1] in linecols: continue
        if pixel[1] - 1 in linecols or pixel[1] + 1 in linecols: continue
        rows.append(pixel[0])
        cols.append(pixel[1])
        colors.append(color)
        rows_taken.append(pixel[0])
    xpose = common.randint(0, 1)
    # Remove that "extra" color that we added just for irrelevant pixels
    linecolors.pop()

  grid, output = common.grids(width, height)
  for linecol, linecolor in zip(linecols, linecolors):
    for r in range(height):
      output[r][linecol] = grid[r][linecol] = linecolor
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color
    for linecol, linecolor in zip(linecols, linecolors):
      if color != linecolor: continue
      output[r][linecol + (-1 if c < linecol else 1)] = color
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=18, linecols=[3, 12], linecolors=[3, 4],
               rows=[3, 3, 7, 10, 11], cols=[1, 6, 9, 7, 16],
               colors=[4, 3, 4, 2, 3], xpose=0),
      generate(width=15, height=14, linecols=[3, 10], linecolors=[2, 1],
               rows=[2, 3, 6, 9, 10, 10], cols=[13, 0, 7, 1, 5, 13],
               colors=[1, 2, 2, 4, 1, 2], xpose=1),
      generate(width=15, height=16, linecols=[5], linecolors=[8],
               rows=[3, 3, 7, 11, 12], cols=[1, 12, 1, 8, 13],
               colors=[1, 8, 8, 8, 1], xpose=1),
  ]
  test = [
      generate(width=26, height=19, linecols=[4, 11, 20], linecolors=[2, 3, 4],
               rows=[2, 4, 5, 7, 9, 10, 11, 15, 15, 15, 17],
               cols=[16, 24, 9, 6, 13, 1, 17, 0, 8, 24, 22],
               colors=[2, 8, 8, 4, 3, 2, 8, 8, 3, 4, 3], xpose=0),
  ]
  return {"train": train, "test": test}
