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


def generate(rows=None, cols=None, brow=None, bcol=None, wide=None, tall=None,
             size=23):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    brow: the horizontal coordinate of the reference sprite
    bcol: the vertical coordinate of the reference sprite
    wide: the width of the reference sprite
    tall: the height of the reference sprite
    size: the width and height of the (square) grid
  """
  def draw(grid, output):
    # If anything looks suspicious, we'll set the following variable to True.
    illegal = False
    # First, draw the input grid -- all yellow dots, plus a blue square.
    for r in range(brow - 1, brow + tall + 1):
      for c in range(bcol - 1, bcol + wide + 1):
        common.draw(grid, r, c, common.blue())
    for r, c in zip(rows, cols):
      grid[r][c] = common.yellow()
    # Second, look for matches.
    matches = []
    for mrow in range(size):
      for mcol in range(size):
        value, xalue = -1, -1
        for rotate in [0, 1, 2, 3]:
          for xpose in [0, 1]:
            match = True
            for r in range(tall):
              for c in range(wide):
                dr, dc = r, c
                if rotate == 1: dr, dc = wide - c - 1, r
                if rotate == 2: dr, dc = tall - r - 1, wide - c - 1
                if rotate == 3: dr, dc = c, tall - r - 1
                if xpose: dr, dc = dc, dr
                mcolor = common.get_pixel(grid, mrow + dr, mcol + dc)
                bcolor = common.get_pixel(grid, brow + r, bcol + c)
                if mcolor == common.blue(): mcolor = common.black()
                if bcolor == common.blue(): bcolor = common.black()
                if mcolor != bcolor: match = False
            if match: value, xalue = rotate, xpose
        if value != -1: matches.append((mrow, mcol, value, xalue))
    # Finally, draw the matches on the output grid, and then the yellow dots.
    # If we see anything weird, we'll set illegal to True.
    for match in matches:
      mrow, mcol, rotate, xpose = match
      w = wide if rotate in [0, 2] else tall
      t = tall if rotate in [0, 2] else wide
      if xpose: w, t = t, w
      for r in range(mrow - 1, mrow + t + 1):
        for c in range(mcol - 1, mcol + w + 1):
          if common.get_pixel(output, r, c) == common.blue(): illegal = True
          if common.get_pixel(grid, r, c) == common.yellow():
            if r in [mrow - 1, mrow + t] or c in [mcol - 1, mcol + w]:
              illegal = True  # There's a pixel on the border of the blue square
          common.draw(output, r, c, common.blue())
    for r, c in zip(rows, cols):
      output[r][c] = common.yellow()
    return not illegal

  if rows is None:
    # Pick a pattern that touches the edges of its border.
    tall, wide = common.randint(1, 3), common.randint(2, 3)
    while True:
      pattern = common.sample(common.all_pixels(wide, tall), max(wide, tall))
      prows, pcols = zip(*pattern)
      if 0 in prows and tall - 1 in prows and 0 in pcols and wide - 1 in pcols:
        break
    num_sprites = common.randint(2, 6)
    while True:  # Keep doing all this until the patterns don't clobber.
      # Draw random static onto a grid.
      grid = common.grid(size, size)
      for r, c in common.random_pixels(size, size, 0.05):
        grid[r][c] = common.yellow()
      # Pick some spots to place the pattern; the last one will be the reference
      for idx in range(num_sprites):
        rotate = common.randint(0, 3) if idx + 1 < num_sprites else 0
        w = wide if rotate in [0, 2] else tall
        t = tall if rotate in [0, 2] else wide
        offset = 0 if idx + 1 < num_sprites else 1
        brow = common.randint(offset, size - t - offset)
        bcol = common.randint(offset, size - w - offset)
        # Clear the space.
        for r in range(brow - 1, brow + t + 1):
          for c in range(bcol - 1, bcol + w + 1):
            common.draw(grid, r, c, common.black())
        for r in range(tall):
          for c in range(wide):
            color = common.yellow() if (r, c) in pattern else common.black()
            dr, dc = r, c
            if rotate == 1: dr, dc = wide - c - 1, r
            if rotate == 2: dr, dc = tall - r - 1, wide - c - 1
            if rotate == 3: dr, dc = c, tall - r - 1
            grid[brow + dr][bcol + dc] = color
      # Extract the colors from the grid.
      rows, cols = [], []
      for r in range(size):
        for c in range(size):
          if not grid[r][c]: continue
          rows.append(r)
          cols.append(c)
      grid, output = common.grids(size, size)
      if draw(grid, output): break  # It worked!

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 2, 3, 4, 4, 5, 7, 8, 12, 13, 13, 14, 14, 15, 18, 20,
                     21],
               cols=[13, 4, 6, 4, 20, 18, 7, 14, 4, 11, 13, 4, 19, 12, 18, 3,
                     11],
               brow=2, bcol=4, wide=3, tall=3),
      generate(rows=[0, 0, 3, 3, 4, 5, 5, 6, 6, 7, 7, 8, 9, 12, 14, 15, 16, 18,
                     19, 19, 20, 21, 22, 22, 22, 22],
               cols=[0, 10, 8, 22, 15, 1, 11, 13, 20, 10, 16, 17, 10, 0, 15, 14,
                     18, 22, 5, 9, 21, 11, 0, 3, 9, 11],
               brow=7, bcol=16, wide=2, tall=2),
      generate(rows=[0, 2, 3, 3, 4, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11,
                     12, 12, 12, 12, 12, 13, 14, 14, 14, 14, 15, 15, 15, 15, 16,
                     16, 17, 17, 17, 18, 18, 19, 19, 20, 22, 22, 22, 22],
               cols=[10, 12, 11, 14, 5, 14, 16, 0, 21, 19, 7, 15, 3, 15, 7, 22,
                     12, 17, 20, 4, 11, 14, 15, 18, 18, 0, 2, 10, 22, 4, 6, 7,
                     10, 17, 21, 2, 9, 12, 1, 13, 16, 22, 21, 2, 10, 14, 18],
               brow=15, bcol=6, wide=2, tall=1),
      generate(rows=[0, 1, 1, 1, 3, 3, 4, 5, 5, 5, 6, 7, 7, 7, 7, 7, 9, 9, 9,
                     11, 11, 11, 11, 12, 12, 13, 13, 14, 14, 16, 16, 17, 17, 18,
                     19, 20, 20, 21, 21, 22],
               cols=[2, 2, 4, 21, 3, 13, 2, 5, 11, 17, 20, 3, 6, 9, 16, 17, 7,
                     8, 12, 0, 5, 7, 18, 1, 22, 4, 19, 5, 13, 11, 22, 3, 10, 2,
                     9, 1, 13, 2, 17, 16],
               brow=9, bcol=7, wide=2, tall=3),
  ]
  test = [
      generate(rows=[1, 1, 3, 3, 3, 4, 5, 8, 9, 9, 10, 10, 11, 11, 11, 12, 16,
                     16, 16, 18, 20, 20, 21, 22, 22],
               cols=[5, 10, 6, 10, 12, 3, 14, 10, 5, 19, 8, 13, 3, 5, 18, 12, 0,
                     7, 18, 19, 6, 8, 21, 1, 6],
               brow=1, bcol=10, wide=3, tall=3),
  ]
  return {"train": train, "test": test}
