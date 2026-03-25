# Copyright 2026 Google LLC
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


def generate(size=None, wides=None, talls=None, brows=None, bcols=None,
             bcolors=None, prows=None, pcols=None, pcolors=None, fcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    bcolors: The colors of the boxes.
    prows: The row of the pixels.
    pcols: The columns of the pixels.
    pcolors: The colors of the pixels.
    fcolor: The color of the frame.
  """

  def draw():
    grid, output = common.grids(size, size, 8)
    # Draw the boxes.
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      common.rect(grid, wide, tall, brow, bcol, bcolor)
      common.rect(output, wide, tall, brow, bcol, bcolor)
    # Draw (and extend) the pixels.
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      row, col = prow, pcol
      for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
          if grid[row + r][col + c] != 8: return None, None  # Not on background
          grid[row + r][col + c] = fcolor
      grid[row][col] = pcolor
      bindex = bcolors.index(pcolor)
      # Keep extending the pixel until it meets the box it belongs to.
      last_dir = -1
      while True:
        for r in [-1, 0, 1]:
          for c in [-1, 0, 1]:
            if row + r < 0 or row + r >= size: return None, None
            if col + c < 0 or col + c >= size: return None, None
            if output[row + r][col + c] not in [8, pcolor]: return None, None
            output[row + r][col + c] = fcolor
        output[row][col] = pcolor
        the_dirs = []
        if row < brows[bindex]: the_dirs.append(1)
        if row >= brows[bindex] + talls[bindex]: the_dirs.append(2)
        if col < bcols[bindex]: the_dirs.append(3)
        if col >= bcols[bindex] + wides[bindex]: the_dirs.append(4)
        if not the_dirs: break
        if len(the_dirs) > 1: return None, None  # Diagonally related, no good.
        if last_dir != -1 and last_dir != the_dirs[0]:
          return None, None  # Changed direction, no good.
        last_dir = the_dirs[0]
        if the_dirs[0] == 1: row += 3
        if the_dirs[0] == 2: row -= 3
        if the_dirs[0] == 3: col += 3
        if the_dirs[0] == 4: col -= 3
    return grid, output

  if size is None:
    size = 20 if common.randint(0, 3) else 25
    boxes = 4 if size == 25 else common.randint(2, 3)
    pixels = boxes + common.randint(0, 1)
    fcolor = common.random_color(exclude=[8])
    bcolors = common.random_colors(boxes, exclude=[8, fcolor])
    while True:
      pcolors = common.choices(bcolors, pixels)
      if len(set(pcolors)) == boxes: break  # need at least one pixel per box
    while True:
      shorts = [common.randint(2, 4) for _ in range(boxes)]
      longs = [common.randint(5, 18) for _ in range(boxes)]
      cdirs = [common.randint(0, 1) for _ in range(boxes)]
      wides = [short if cdir else long for short, long, cdir in zip(shorts, longs, cdirs)]
      talls = [long if cdir else short for short, long, cdir in zip(shorts, longs, cdirs)]
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      prows = [common.randint(2, size - 3) for _ in range(pixels)]
      pcols = [common.randint(2, size - 3) for _ in range(pixels)]
      the_rows = brows + [prow - 1 for prow in prows]
      the_cols = bcols + [pcol - 1 for pcol in pcols]
      the_wides = wides + [3] * pixels
      the_talls = talls + [3] * pixels
      if common.overlaps(the_rows, the_cols, the_wides, the_talls, 1): continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, wides=[4, 2], talls=[11, 10], brows=[9, 0], bcols=[1, 16], bcolors=[2, 4], prows=[4, 13], pcols=[4, 13], pcolors=[4, 2], fcolor=1),
      generate(size=20, wides=[3, 2, 12], talls=[5, 8, 4], brows=[0, 3, 16], bcols=[5, 1, 6], bcolors=[3, 1, 4], prows=[4, 8, 13], pcols=[13, 8, 14], pcolors=[3, 1, 4], fcolor=2),
      generate(size=20, wides=[13, 3], talls=[3, 12], brows=[1, 5], bcols=[2, 16], bcolors=[3, 6], prows=[9, 10, 14], pcols=[4, 10, 4], pcolors=[3, 6, 6], fcolor=4),
  ]
  test = [
      generate(size=25, wides=[9, 10, 6, 3], talls=[2, 2, 18, 17], brows=[1, 1, 5, 7], bcols=[1, 13, 19, 1], bcolors=[1, 2, 4, 3], prows=[8, 11, 14, 16, 20], pcols=[16, 8, 13, 9, 13], pcolors=[4, 1, 2, 3, 4], fcolor=9),
  ]
  return {"train": train, "test": test}
