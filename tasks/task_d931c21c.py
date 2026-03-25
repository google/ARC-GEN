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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    colors: A list of colors to use.
  """

  if width is None:
    base = common.randint(10, 28)
    width, height = base + common.randint(-2, 2), base + common.randint(-2, 2)
    num_boxes = base // 5
    # Determine the boundaries of all boxes.
    while True:
      ws = [common.randint(1, min(10, width - 5)) for _ in range(num_boxes)]
      ts = [common.randint(1, min(10, height - 5)) for _ in range(num_boxes)]
      rs = [common.randint(1, height - tall - 1) for tall in ts]
      cs = [common.randint(1, width - wide - 1) for wide in ws]
      if not common.overlaps(rs, cs, ws, ts, 4): break
    # Determine the contents of all boxes.
    brows, bcols, wides, talls, holes, halos = [], [], [], [], [], []
    for wide, tall, row, col in zip(ws, ts, rs, cs):
      holey = common.randint(0, 1)
      if wide > 2 and tall > 1 and common.randint(0, 1):  # Split left/right
        while True:
          wide_left = common.randint(1, wide - 1)
          wide_rite = wide - wide_left
          tall_left = common.randint(1, tall)
          tall_rite = common.randint(1, tall)
          row_left = common.randint(row, row + tall - tall_left)
          row_rite = common.randint(row, row + tall - tall_rite)
          # Make sure they aren't identical (thus appearring as one).
          if row_left == row_rite and tall_left == tall_rite: continue
          # Make sure they line up such that their insides connect.
          if row_left + tall_left <= row_rite: continue
          if row_rite + tall_rite <= row_left: continue
          # If they line up perfectly, make sure we create the tinest chunk.
          if row_left == row_rite or row_left + tall_left == row_rite + tall_rite:
            if tall_rite < tall_left:
              area_mine = wide_rite * tall_rite
              area_other = wide_left * (tall_left - tall_rite)
              if area_mine >= area_other: continue
            if tall_rite > tall_left:
              area_mine = wide_left * tall_left
              area_other = wide_rite * (tall_rite - tall_left)
              if area_mine >= area_other: continue
          break
        brows.extend([row_left, row_rite])
        bcols.extend([col, col + wide_left])
        wides.extend([wide_left, wide_rite])
        talls.extend([tall_left, tall_rite])
        hs = [0, 0]
        if holey:
          hs[common.randint(0, 1)] += 1
          hs[common.randint(0, 1)] += 1
        holes.extend(hs)
        halos.extend([1 - holey, 1 - holey])
        continue
      if tall > 2 and wide > 1 and common.randint(0, 1):  # Split above/below
        while True:
          tall_above = common.randint(1, tall - 1)
          tall_below = tall - tall_above
          wide_above = common.randint(1, wide)
          wide_below = common.randint(1, wide)
          col_above = common.randint(col, col + wide - wide_above)
          col_below = common.randint(col, col + wide - wide_below)
          # Make sure they aren't identical (thus appearring as one).
          if col_above == col_below and wide_above == wide_below: continue
          # Make sure they line up such that their insides connect.
          if col_above + wide_above <= col_below: continue
          if col_below + wide_below <= col_above: continue
          # If they line up perfectly, make sure we create the tinest chunk.
          if col_above == col_below or col_above + wide_above == col_below + wide_below:
            if wide_below < wide_above:
              area_mine = tall_below * wide_below
              area_other = tall_above * (wide_above - wide_below)
              if area_mine >= area_other: continue
            if wide_below > wide_above:
              area_mine = tall_above * wide_above
              area_other = tall_below * (wide_below - wide_above)
              if area_mine >= area_other: continue
          break
        brows.extend([row, row + tall_above])
        bcols.extend([col_above, col_below])
        wides.extend([wide_above, wide_below])
        talls.extend([tall_above, tall_below])
        hs = [0, 0]
        if holey:
          hs[common.randint(0, 1)] += 1
          hs[common.randint(0, 1)] += 1
        holes.extend(hs)
        halos.extend([1 - holey, 1 - holey])
        continue
      brows.append(row)
      bcols.append(col)
      wides.append(wide)
      talls.append(tall)
      holes.append(holey * common.randint(1, 2))
      halos.append(1 - holey)
    colors = common.grid(width, height)
    # Draw the red boxes.
    for brow, bcol, wide, tall, halo in zip(brows, bcols, wides, talls, halos):
      common.hollow_rect(colors, wide + 4, tall + 4, brow - 2, bcol - 2, 2 if halo else 0)
    # Draw the blue boxes.
    for brow, bcol, wide, tall in zip(brows, bcols, wides, talls):
      common.hollow_rect(colors, wide + 2, tall + 2, brow - 1, bcol - 1, 1)
    # Draw the green boxes.
    for brow, bcol, wide, tall, halo in zip(brows, bcols, wides, talls, halos):
      common.hollow_rect(colors, wide, tall, brow, bcol, 3 if halo else 0)
    # Draw the black insides.
    for brow, bcol, wide, tall in zip(brows, bcols, wides, talls):
      common.rect(colors, wide - 2, tall - 2, brow + 1, bcol + 1, 0)
    # Draw the holes.
    for brow, bcol, wide, tall, hole in zip(brows, bcols, wides, talls, holes):
      for _ in range(hole):
        while True:
          r = common.randint(brow - 1, brow + tall + 1)
          c = common.randint(bcol - 1, bcol + wide + 1)
          if common.get_pixel(colors, r, c - 1) == 1 and common.get_pixel(colors, r, c) == 1 and common.get_pixel(colors, r, c + 1) == 1:
            colors[r][c] = 0
            break
          if common.get_pixel(colors, r - 1, c) == 1 and common.get_pixel(colors, r, c) == 1 and common.get_pixel(colors, r + 1, c) == 1:
            colors[r][c] = 0
            break
    colors = common.flatten(colors)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = color
    if color == 1: grid[i // width][i % width] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=16,
               colors=[0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0,
                       0, 0, 2, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 0,
                       0, 0, 2, 1, 3, 0, 0, 3, 1, 1, 1, 1, 2, 0,
                       0, 0, 2, 1, 3, 0, 0, 3, 3, 3, 3, 1, 2, 0,
                       0, 0, 2, 1, 3, 3, 3, 3, 3, 0, 3, 1, 2, 0,
                       0, 0, 2, 1, 1, 1, 1, 1, 3, 0, 3, 1, 2, 0,
                       0, 0, 2, 2, 2, 2, 2, 1, 3, 3, 3, 1, 2, 0,
                       0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 0,
                       0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 2,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 1, 2,
                       0, 0, 0, 1, 0, 1, 1, 1, 0, 2, 1, 1, 1, 2,
                       0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 2, 2, 2, 2,
                       0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=10, height=9,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 1, 1, 1, 0, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=22, height=19,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 1, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 1, 3, 3, 3, 0, 3, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0,
                       0, 0, 2, 1, 1, 1, 3, 0, 3, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,
                       0, 0, 2, 2, 2, 1, 3, 3, 3, 1, 2, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0,
                       1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 1, 1, 3, 3, 1, 2, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 1, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=8, height=8,
               colors=[2, 2, 2, 1, 1, 1, 2, 0,
                       2, 1, 1, 1, 3, 1, 2, 0,
                       2, 1, 3, 3, 3, 1, 2, 0,
                       2, 1, 3, 0, 3, 1, 2, 0,
                       2, 1, 3, 3, 3, 1, 2, 0,
                       2, 1, 1, 1, 1, 1, 2, 0,
                       2, 2, 2, 2, 2, 2, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=30, height=30,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 1,
                       0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 1, 3, 0, 3, 1,
                       0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 2, 1, 1, 3, 0, 3, 1,
                       0, 0, 0, 0, 2, 1, 3, 3, 3, 1, 1, 1, 2, 0, 0, 0, 0, 2, 1, 3, 1, 2, 0, 2, 1, 3, 3, 3, 3, 1,
                       0, 0, 0, 0, 2, 1, 3, 0, 3, 3, 3, 1, 2, 0, 0, 0, 0, 2, 1, 3, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1,
                       0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 2, 1, 1, 1, 2, 0, 2, 2, 2, 2, 2, 2, 2,
                       0, 0, 0, 0, 2, 1, 1, 1, 1, 3, 3, 1, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 2, 2, 2, 1, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 3, 3, 3, 1, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 1, 1, 3, 3, 1, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 3, 3, 1, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
