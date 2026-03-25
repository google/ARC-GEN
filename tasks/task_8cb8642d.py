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


def generate(width=None, height=None, wides=None, talls=None, rows=None,
             cols=None, bgcolors=None, fgcolors=None, corners=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    bgcolors: The background colors of the boxes.
    fgcolors: The foreground colors of the boxes.
    corners: The corners of the pixels.
  """

  if width is None:
    width, height = common.randint(10, 25), common.randint(10, 25)
    num_boxes = 1
    if width * height > 200: num_boxes = 2
    if width * height > 300: num_boxes = 3
    while True:
      wides = [common.randint(5, width - 2) for _ in range(num_boxes)]
      talls = [common.randint(5, height - 2) for _ in range(num_boxes)]
      bads = sum([1 if (w > t and t % 2 == 0) or (t > w and w % 2 == 0) else 0 for w, t in zip(wides, talls)])
      if bads: continue
      rows = [common.randint(1, height - tall - 1) for tall in talls]
      cols = [common.randint(1, width - wide - 1) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break
    bgcolors = common.random_colors(num_boxes)
    fgcolors = []
    for bgcolor in bgcolors:
      fgcolors.append(common.random_color(exclude=[bgcolor]))
    corners = [common.randint(0, 3) for _ in range(num_boxes)]

  grid, output = common.grids(width, height)
  for wide, tall, row, col, bgcolor, fgcolor, corner in zip(wides, talls, rows, cols, bgcolors, fgcolors, corners):
    common.rect(grid, wide, tall, row, col, bgcolor)
    r = (row + 1) if corner in [0, 1] else (row + tall - 2)
    c = (col + 1) if corner in [0, 2] else (col + wide - 2)
    grid[r][c] = fgcolor
    for r in range(tall):
      for c in range(wide):
        draw = False
        if r <= tall // 2 and c <= wide // 2 and r == c: draw = True
        if r <= tall // 2 and c >= wide // 2 and r == (wide - 1 - c): draw = True
        if r >= tall // 2 and c <= wide // 2 and (tall - 1 - r) == c: draw = True
        if r >= tall // 2 and c >= wide // 2 and (tall - 1 - r) == (wide - 1 - c): draw = True
        if wide > tall and c > tall // 2 and c + tall // 2 < wide and r == tall // 2: draw = True
        if tall > wide and r > wide // 2 and r + wide // 2 < tall and c == wide // 2: draw = True
        if draw: output[row + r][col + c] = fgcolor
    common.hollow_rect(output, wide, tall, row, col, bgcolor)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=13, wides=[9], talls=[10], rows=[1], cols=[2], bgcolors=[3], fgcolors=[6], corners=[1]),
      generate(width=15, height=12, wides=[8], talls=[7], rows=[1], cols=[1], bgcolors=[2], fgcolors=[1], corners=[0]),
      generate(width=18, height=17, wides=[7, 6, 11], talls=[7, 6, 7], rows=[1, 1, 9], cols=[2, 11, 6], bgcolors=[1, 3, 4], fgcolors=[2, 2, 3], corners=[3, 1, 2]),
  ]
  test = [
      generate(width=24, height=19, wides=[6, 9, 10], talls=[6, 13, 10], rows=[1, 2, 8], cols=[1, 14, 3], bgcolors=[3, 8, 2], fgcolors=[1, 6, 4], corners=[2, 0, 2]),
  ]
  return {"train": train, "test": test}
