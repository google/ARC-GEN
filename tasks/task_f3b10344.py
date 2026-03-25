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
             bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row indices of the tops of the rectangles.
    bcols: The column indices of the left sides of the rectangles.
    colors: The colors of the rectangles.
  """

  def draw(debug=False):
    if min([colors.count(color) for color in colors]) < 2:
      if debug: print("Not enough colors")
      return None, None
    if common.overlaps(brows, bcols, wides, talls, 1):
      if debug: print("Overlaps")
      return None, None
    grid, output = common.grids(width, height)
    def get_info(wide, tall, row, col, hue):
      me, cyan, clobber = False, False, False
      for r in range(tall):
        for c in range(wide):
          color = common.get_pixel(output, row + r, col + c)
          if color == hue: me = True
          if color == 8: cyan = True
          if color not in [0, 8, hue]: clobber = True
      if clobber: return 2  # Major problem!
      if cyan and not me: return 2  # Also a problem (don't cross streams).
      return 1 if me else 0  # 1 = don't draw, 0 = draw
    for wide, tall, brow, bcol, color in zip(wides, talls, brows, bcols, colors):
      common.rect(grid, wide, tall, brow, bcol, color)
      common.rect(output, wide, tall, brow, bcol, color)
    for j in range(len(wides)):
      for i in range(j):
        if colors[i] != colors[j]: continue
        if common.isclose(brows[i] + talls[i] / 2, brows[j] + talls[j] / 2):
          left = min(bcols[i] + wides[i], bcols[j] + wides[j])
          right = max(bcols[i], bcols[j])
          top = max(brows[i], brows[j]) + 1
          bottom = min(brows[i] + talls[i], brows[j] + talls[j]) - 1
          wide, tall = right - left, bottom - top
          info = get_info(wide, tall, top, left, colors[i])
          if info == 0: common.rect(output, wide, tall, top, left, 8)
          if info == 2:
            if debug: print("Bad info")
            return None, None
        if common.isclose(bcols[i] + wides[i] / 2, bcols[j] + wides[j] / 2):
          top = min(brows[i] + talls[i], brows[j] + talls[j])
          bottom = max(brows[i], brows[j])
          left = max(bcols[i], bcols[j]) + 1
          right = min(bcols[i] + wides[i], bcols[j] + wides[j]) - 1
          wide, tall = right - left, bottom - top
          info = get_info(wide, tall, top, left, colors[i])
          if info == 0: common.rect(output, wide, tall, top, left, 8)
          if info == 2:
            if debug: print("Bad info")
            return None, None
    return grid, output

  if width is None:
    subset = common.random_colors(common.randint(2, 3), exclude=[8])
    expected_boxes = 2 * len(subset) + common.randint(1, 5)
    while True:
      width, height = common.randint(25, 30), common.randint(25, 30)
      wides, talls, brows, bcols, colors = [], [], [], [], []
      def process(wide, tall, brow, bcol, color):
        if brow < 0 or brow + tall > height or bcol < 0 or bcol + wide > width:
          return
        wides.append(wide)
        talls.append(tall)
        brows.append(brow)
        bcols.append(bcol)
        colors.append(color)
        for rdir, cdir in [(0, 1), (1, 0)]:
          w, t = common.randint(3, 9), common.randint(3, 9)
          r, c = common.randint(0, height - t), common.randint(0, width - w)
          if rdir:
            if w % 2 != wide % 2: w += 1
            c = bcol + (wide - w) // 2
          if cdir:
            if t % 2 != tall % 2: t += 1
            r = brow + (tall - t) // 2
          if not common.overlaps(brows + [r], bcols + [c], wides + [w], talls + [t], 1):
            process(w, t, r, c, color)
      for color in subset:
        wide, tall = common.randint(3, 9), common.randint(3, 9)
        brow = common.randint(0, height - tall)
        bcol = common.randint(0, width - wide)
        process(wide, tall, brow, bcol, color)
      if len(colors) != expected_boxes: continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=30, wides=[6, 5, 6, 6, 6, 4, 4],
               talls=[7, 7, 7, 6, 4, 4, 4], brows=[1, 1, 1, 14, 15, 15, 21],
               bcols=[4, 14, 22, 22, 4, 14, 5], colors=[2, 6, 6, 6, 2, 2, 2]),
      generate(width=30, height=30, wides=[7, 5, 5, 5, 5],
               talls=[7, 7, 6, 5, 5], brows=[4, 4, 14, 22, 22],
               bcols=[3, 20, 7, 7, 20], colors=[1, 1, 3, 3, 3]),
      generate(width=30, height=25, wides=[7, 6, 3, 6, 3, 3, 5, 7, 6],
               talls=[6, 6, 4, 4, 4, 3, 3, 3, 3],
               brows=[2, 2, 3, 11, 11, 12, 12, 17, 17],
               bcols=[4, 16, 24, 16, 24, 0, 5, 4, 16],
               colors=[4, 4, 4, 6, 6, 4, 4, 4, 6]),
  ]
  test = [
      generate(width=29, height=30, wides=[7, 6, 3, 5, 6, 4, 9, 6, 3, 3, 3],
               talls=[5, 5, 3, 5, 5, 5, 5, 5, 3, 3, 3],
               brows=[1, 1, 2, 10, 10, 10, 19, 19, 20, 26, 26],
               bcols=[5, 16, 1, 6, 16, 24, 4, 16, 24, 9, 14],
               colors=[7, 7, 7, 7, 3, 3, 7, 3, 3, 2, 2]),
  ]
  return {"train": train, "test": test}
