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


def generate(wides=None, talls=None, brows=None, bcols=None, fgcolors=None,
             bgcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    fgcolors: The foreground colors of the boxes.
    bgcolors: The background colors of the boxes.
  """

  def draw():
    overlaps = False
    # Draw the boxes and pixels.
    grid, output = common.grids(20, 20)
    for wide, tall, brow, bcol, fg, bg in zip(wides, talls, brows, bcols,
                                              fgcolors, bgcolors):
      for r in range(brow, brow + tall):
        for c in range(bcol, bcol + wide):
          if output[r][c] != 0: overlaps = True
          grid[r][c] = 0
          output[r][c] = bg
      for r in range(1, tall, 2):
        for c in range(1, wide, 2):
          grid[brow + r][bcol + c] = fg
          output[brow + r][bcol + c] = fg
    if not overlaps: return None, None  # We expect at least a little overlap.
    # Draw the legend.
    for i, (fg, bg) in enumerate(zip(fgcolors, bgcolors)):
      grid[len(wides) - 1 - i][0] = fg
      grid[len(wides) - 1 - i][1] = bg
      if grid[len(wides) - 1 - i][2] != 0: return None, None
      if output[len(wides) - 1 - i][2] != 0: return None, None
    # Make sure the legend isn't covering up anything.
    for c in range(3):
      if grid[len(wides)][c] != 0: return None, None
      if output[len(wides)][c] != 0: return None, None
    # Make sure at least three corners of each box are visible.
    for wide, tall, brow, bcol, bg in zip(wides, talls, brows, bcols, bgcolors):
      corners = 0
      if output[brow][bcol] == bg: corners += 1
      if output[brow + tall - 1][bcol] == bg: corners += 1
      if output[brow][bcol + wide - 1] == bg: corners += 1
      if output[brow + tall - 1][bcol + wide - 1] == bg: corners += 1
      if corners < 3: return None, None
    # Make sure at least three corner pixels in each box are visible.
    for wide, tall, brow, bcol, fg in zip(wides, talls, brows, bcols, fgcolors):
      corners = 0
      if grid[brow + 1][bcol + 1] == fg: corners += 1
      if grid[brow + tall - 2][bcol + 1] == fg: corners += 1
      if grid[brow + 1][bcol + wide - 2] == fg: corners += 1
      if grid[brow + tall - 2][bcol + wide - 2] == fg: corners += 1
      if corners < 3: return None, None
    # Make sure no box abuts another, or overlaps another by a *single* pixel.
    # That leads to ambiguity (e.g., which one should be drawn in the
    # foreground).
    for i in range(len(wides)):
      for j in range(i):
        if brows[i] + talls[i] < brows[j]: continue
        if bcols[i] + wides[i] < bcols[j]: continue
        if brows[j] + talls[j] < brows[i]: continue
        if bcols[j] + wides[j] < bcols[i]: continue
        if brows[i] + talls[i] - brows[j] == 1: return None, None
        if bcols[i] + wides[i] - bcols[j] == 1: return None, None
        if brows[j] + talls[j] - brows[i] == 1: return None, None
        if bcols[j] + wides[j] - bcols[i] == 1: return None, None
    return grid, output

  if wides is None:
    boxes = common.randint(2, 3)
    fgcolors = common.random_colors(boxes)
    bgcolors = common.random_colors(boxes)
    while True:
      wides = [2 * common.randint(2, 7) + 1 for _ in range(boxes)]
      talls = [2 * common.randint(2, 7) + 1 for _ in range(boxes)]
      brows = [common.randint(0, 20 - t) for t in talls]
      bcols = [common.randint(0, 20 - w) for w in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[9, 7, 7], talls=[9, 15, 9], brows=[7, 3, 9],
               bcols=[10, 3, 7], fgcolors=[4, 8, 5], bgcolors=[3, 7, 6]),
      generate(wides=[9, 5], talls=[17, 9], brows=[3, 9], bcols=[5, 2],
               fgcolors=[8, 4], bgcolors=[7, 1]),
      generate(wides=[11, 7, 5], talls=[9, 11, 5], brows=[0, 3, 13],
               bcols=[3, 5, 14], fgcolors=[7, 8, 1], bgcolors=[8, 1, 3]),
  ]
  test = [
      generate(wides=[5, 9, 7], talls=[9, 7, 9], brows=[11, 7, 9],
               bcols=[0, 6, 12], fgcolors=[4, 5, 8], bgcolors=[9, 1, 4]),
  ]
  return {"train": train, "test": test}
