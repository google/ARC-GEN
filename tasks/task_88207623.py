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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, sides=None, ysides=None, idxs=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row offsets of the rectangles.
    bcols: The column offsets of the rectangles.
    sides: Whether the rectangles are on the left or right.
    ysides: Whether the rectangles are on the top or bottom.
    idxs: The indices of the last colors in the rectangles.
    colors: The colors of the rectangles.
  """

  def draw():
    grid, output = common.grids(width, height)
    offset = 0
    for wide, tall, brow, bcol, side, idx in zip(wides, talls, brows, bcols, sides, idxs):
      for row in range(tall):
        output[brow + row][bcol] = grid[brow + row][bcol] = 2
      for row in range(tall):
        for col in range(wide):
          i = row * wide + col
          color = int(colors[offset + i])
          lcolor = color if side else (4 if color else 0)
          rcolor = (4 if color else 0) if side else color
          if side:
            grid[brow + row][bcol + 1 + col] = rcolor
            if i == idx: grid[brow + row][bcol - 1 - col] = lcolor
          else:
            grid[brow + row][bcol - 1 - col] = lcolor
            if i == idx: grid[brow + row][bcol + 1 + col] = rcolor
          output[brow + row][bcol + 1 + col] = rcolor
          output[brow + row][bcol - 1 - col] = lcolor
      offset += wide * tall
    return grid, output

  if width is None:
    width, height = 16, 16
    whatever = common.randint(0, 2)
    if whatever == 0: width = 14 if common.randint(0, 1) else 18
    if whatever == 1: height = 14 if common.randint(0, 1) else 18
    num_boxes = common.randint(2, 4)
    subset = common.random_colors(num_boxes, exclude=[2, 4])
    while True:
      wides = [common.randint(2, 5) for _ in range(num_boxes)]
      talls = [common.randint(3, 6) for _ in range(num_boxes)]
      brows = [common.randint(1, height - tall - 1) for tall in talls]
      bcols = [common.randint(wide, width - wide - 1) for wide in wides]
      sides = [common.randint(0, 1) for _ in range(num_boxes)]
      if len(set(bcols)) != len(bcols): continue  # Let's keep cols unique.
      # Check that the expanded rectangles do not overlap.
      ocols = [bcol - wide for bcol, wide in zip(bcols, wides)]
      owides = [2 * wide + 1 for wide in wides]
      if common.overlaps(brows, ocols, owides, talls): continue
      # Check that the drawn rectangles don't come close to overlapping at all.
      ocols = [bcol if side else (bcol - wide) for bcol, wide, side in zip(bcols, wides, sides)]
      owides = [wide + 1 for wide in wides]
      if common.overlaps(brows, ocols, owides, talls, 1): continue
      # Choose the sprite shapes.
      colors, idxs = [], []
      for idx, (wide, tall) in enumerate(zip(wides, talls)):
        pixels = common.diagonally_connected_sprite(wide, tall, wide + tall)
        for row in range(tall):
          for col in range(wide):
            colors.append(subset[idx] if (row, col) in pixels else 0)
        row, col = common.choice(pixels)
        idxs.append(row * wide + col)
      colors = "".join(map(str, colors))
      break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=16, wides=[5, 5], talls=[6, 4], brows=[1, 11],
               bcols=[6, 5], sides=[1, 0], idxs=[21, 13],
               colors="00050055055555055000555005000070000777007077707770"),
      generate(width=16, height=14, wides=[3, 4], talls=[6, 4], brows=[1, 9],
               bcols=[6, 11], sides=[0, 0], idxs=[8, 5],
               colors="8008888888888808003000030030330330"),
  ]
  test = [
      generate(width=18, height=16, wides=[4, 3, 4, 2], talls=[3, 4, 6, 3],
               brows=[1, 3, 7, 12], bcols=[4, 13, 6, 14], sides=[0, 0, 0, 1],
               idxs=[1, 11, 14, 5],
               colors="111001101111800888080888000700700700777077070700300333"),
  ]
  return {"train": train, "test": test}
