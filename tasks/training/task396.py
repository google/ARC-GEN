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


def generate(width=None, height=None, rows=None, cols=None, brows=None,
             bcols=None, wides=None, talls=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    brows: a list of vertical coordinates where the boxes should be placed
    bcols: a list of horizontal coordinates where the boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    colors: a pair of digits representing the colors to use
  """
  if width is None:
    width, height = common.randint(12, 18), common.randint(12, 18)
    num_boxes, colors = common.randint(2, 3), common.random_colors(2)
    # Choose non-overlapping positions for the boxes.
    while True:
      wides = sorted(common.sample(range(3, 9), num_boxes), reverse=True)
      talls = sorted(common.sample(range(3, 9), num_boxes), reverse=True)
      counts = sorted(common.sample(range(0, 5), num_boxes), reverse=True)
      if [c for c, w, t in zip(counts, wides, talls) if c > (w - 2) * (t - 2)]:
        continue   # Can't have more pixels in a box than its area.
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    # Draw random static on the grid.
    pixels = common.random_pixels(width, height, 0.05)
    grid = common.grid(width, height)
    for r, c in pixels:
      grid[r][c] = colors[1]
    # Draw the boxes onto the grid.
    for idx in range(len(brows)):
      brow, bcol, wide, tall = brows[idx], bcols[idx], wides[idx], talls[idx]
      for r in range(tall):
        for c in range(wide):
          grid[brow + r][bcol + c] = colors[0]
      for r in range(1, tall - 1):
        for c in range(1, wide - 1):
          grid[brow + r][bcol + c] = common.black()
    # Choose and draw the box pixels.
    for idx in range(len(brows)):
      brow, bcol, wide, tall = brows[idx], bcols[idx], wides[idx], talls[idx]
      pixels = common.sample(common.all_pixels(wide - 2, tall - 2), counts[idx])
      for p in pixels:
        grid[brow + 1 + p[0]][bcol + 1 + p[1]] = colors[1]
    # Extract the pixels back into rows & columns.
    rows, cols = [], []
    for r in range(height):
      for c in range(width):
        if grid[r][c] == colors[1]:
          rows.append(r)
          cols.append(c)

  grid, output = common.grid(width, height), common.grid(wides[0], talls[0])
  # Draw the boxes.
  for idx in range(len(brows)):
    brow, bcol, wide, tall = brows[idx], bcols[idx], wides[idx], talls[idx]
    for r in range(tall):
      for c in range(wide):
        grid[brow + r][bcol + c] = colors[0]
        if not idx: output[r][c] = colors[1]
    for r in range(1, tall - 1):
      for c in range(1, wide - 1):
        grid[brow + r][bcol + c] = common.black()
        if not idx: output[r][c] = common.black()
  # Draw the static.
  for r, c in zip(rows, cols):
    grid[r][c] = colors[1]
    if r < brows[0] or r >= brows[0] + talls[0]: continue
    if c < bcols[0] or c >= bcols[0] + wides[0]: continue
    output[r - brows[0]][c - bcols[0]] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13,
               rows=[0, 0, 4, 6, 9, 9, 10, 12, 12],
               cols=[4, 12, 1, 4, 4, 10, 9, 4, 11],
               brows=[2, 3], bcols=[0, 10], wides=[7, 3], talls=[7, 4],
               colors=[2, 4]),
      generate(width=16, height=13,
               rows=[0, 1, 2, 3, 4, 4, 5, 5, 5, 9, 11, 11, 12, 12, 12, 12],
               cols=[13, 4, 3, 11, 1, 5, 6, 9, 11, 5, 0, 11, 0, 7, 10, 11],
               brows=[2, 7], bcols=[8, 1], wides=[7, 6], talls=[6, 5],
               colors=[1, 3]),
      generate(width=16, height=15,
               rows=[0, 1, 2, 2, 4, 4, 5, 6, 9, 10, 10, 12, 13, 14],
               cols=[8, 10, 3, 5, 8, 12, 3, 6, 12, 7, 15, 11, 2, 8],
               brows=[1, 3, 10], bcols=[1, 10, 3], wides=[7, 4, 3],
               talls=[7, 5, 4], colors=[3, 2]),
  ]
  test = [
      generate(width=17, height=17,
               rows=[0, 2, 2, 2, 3, 3, 4, 6, 6, 7, 8, 9, 10, 11, 13, 13, 13, 14,
                     14, 14, 16, 16, 16],
               cols=[14, 6, 8, 12, 12, 14, 14, 6, 16, 9, 13, 1, 5, 1, 5, 11, 13,
                     3, 4, 7, 8, 9, 16],
               brows=[1, 11, 2], bcols=[4, 10, 0], wides=[8, 6, 3],
               talls=[8, 5, 3], colors=[1, 8]),
  ]
  return {"train": train, "test": test}
