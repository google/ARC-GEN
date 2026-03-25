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
             bcols=None, bgcolors=None, fgcolors=None, prows=None, pcols=None,
             pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The row indices of the tops of the boxes.
    bcols: The column indices of the left sides of the boxes.
    bgcolors: The background colors of the boxes.
    fgcolors: The foreground colors of the boxes.
    prows: The row indices of the pixels.
    pcols: The column indices of the pixels.
    pcolors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height)
    for wide, tall, brow, bcol, bgcolor, fgcolor in zip(wides, talls, brows, bcols, bgcolors, fgcolors):
      common.hollow_rect(grid, wide, tall, brow, bcol, bgcolor)
      common.hollow_rect(output, wide, tall, brow, bcol, bgcolor)
      # Temporarily fill in the inside with -1
      common.hollow_rect(grid, wide - 2, tall - 2, brow + 1, bcol + 1, -1)
      for row in range(tall - 2):
        for col in range(wide - 2):
          if row % 2 == col % 2:
            output[brow + row + 1][bcol + col + 1] = fgcolor
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      if grid[prow][pcol] != 0: return None, None
      grid[prow][pcol] = pcolor
    # Clean up the temporary -1s.
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      common.hollow_rect(grid, wide - 2, tall - 2, brow + 1, bcol + 1, 0)
    return grid, output

  if width is None:
    width, height = common.randint(10, 30), common.randint(10, 30)
    num_boxes = 2 if min(width, height) <= 20 else 3
    bgcolors = common.random_colors(num_boxes)
    fgcolors = common.random_colors(num_boxes, exclude=bgcolors)
    while True:
      wides = [common.randint(3, width // 2) for _ in range(num_boxes)]
      talls = [common.randint(3, height // 2) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      num_pixels = [((wide - 2) * (tall - 2) + 1) // 2 for wide, tall in zip(wides, talls)]
      if len(set(num_pixels)) != len(num_pixels): continue
      prows, pcols, pcolors = [], [], []
      for num_pixels, fgcolor in zip(num_pixels, fgcolors):
        for _ in range(num_pixels):
          prows.append(common.randint(0, height - 1))
          pcols.append(common.randint(0, width - 1))
          pcolors.append(fgcolor)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=20, height=20, wides=[5, 9], talls=[5, 4], brows=[1, 10],
               bcols=[2, 9], bgcolors=[2, 3], fgcolors=[8, 4],
               prows=[0, 1, 3, 5, 7, 7, 8, 8, 13, 17, 17, 18],
               pcols=[18, 10, 17, 11, 1, 14, 6, 19, 4, 2, 11, 17],
               pcolors=[8, 8, 4, 4, 4, 8, 4, 4, 8, 4, 8, 4]),
      generate(width=23, height=18, wides=[7, 7], talls=[4, 8], brows=[1, 6],
               bcols=[1, 14], bgcolors=[8, 4], fgcolors=[3, 6],
               prows=[0, 1, 2, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 13, 15, 16, 16, 16, 17],
               pcols=[10, 14, 16, 20, 11, 11, 9, 3, 7, 1, 5, 10, 1, 5, 10, 4, 1, 10, 19, 14],
               pcolors=[6, 6, 6, 6, 3, 6, 6, 6, 3, 6, 6, 3, 6, 3, 6, 6, 3, 6, 6, 6]),
      generate(width=20, height=12, wides=[3, 5], talls=[3, 3], brows=[1, 7],
               bcols=[1, 3], bgcolors=[1, 8], fgcolors=[4, 2], prows=[1, 4, 7],
               pcols=[7, 15, 12], pcolors=[2, 4, 2]),
  ]
  test = [
      generate(width=26, height=22, wides=[9, 11, 4], talls=[6, 8, 4],
               brows=[1, 9, 10], bcols=[3, 11, 2], bgcolors=[1, 3, 2],
               fgcolors=[4, 5, 8],
               prows=[0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 9, 10, 10, 10, 12, 12, 15, 15, 15, 16, 17, 18, 18, 18, 19, 19, 19, 19, 20, 20, 21, 21, 21, 21],
               pcols=[1, 17, 12, 14, 22, 0, 18, 13, 16, 21, 1, 24, 14, 21, 0, 18, 14, 24, 7, 3, 0, 8, 23, 10, 24, 1, 5, 7, 25, 7, 2, 15, 19, 1, 10, 13, 23, 5, 18, 5, 12, 19, 21],
               pcolors=[5, 4, 5, 5, 5, 5, 5, 5, 4, 4, 5, 5, 4, 5, 4, 4, 5, 4, 5, 5, 5, 4, 5, 5, 4, 4, 5, 5, 5, 4, 8, 5, 5, 5, 5, 5, 4, 5, 4, 8, 4, 5, 5]),
  ]
  return {"train": train, "test": test}
