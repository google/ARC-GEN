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


def generate(width=None, height=None, bgcolor=None, wides=None, talls=None,
             brows=None, bcols=None, bcolors=None, prows=None, pcols=None,
             pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    bgcolor: The background color of the grid.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row indices of the tops of the rectangles.
    bcols: The column indices of the left sides of the rectangles.
    bcolors: The colors of the rectangles.
    prows: The row indices of the tops of the patterns.
    pcols: The column indices of the left sides of the patterns.
    pcolors: The colors of the patterns.
  """

  def draw():
    if common.overlaps(brows, bcols, wides, talls, 1): return None, None
    grid, output = common.grids(width, height, bgcolor)
    def put(g, r, c, color):
      if g[r][c] != bgcolor: return False
      g[r][c] = color
      return True
    for wide, tall, brow, bcol, bcolor in zip(wides, talls, brows, bcols, bcolors):
      common.rect(grid, wide, tall, brow, bcol, bcolor)
      common.rect(output, wide, tall, brow, bcol, bcolor)
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      if not put(grid, prow, pcol, pcolor): return None, None
      for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        if not put(output, prow + dr, pcol + dc, pcolor): return None, None
      idx, rows, cols = bcolors.index(pcolor), [], []
      if pcol >= bcols[idx] + wides[idx]:
        rows, cols = [prow - 1, prow + 1], [bcols[idx] + wides[idx]] * 2
        for c in range(bcols[idx] + wides[idx], pcol - 1):
          if not put(output, prow, c, pcolor): return None, None
      if pcol < bcols[idx]:
        rows, cols = [prow - 1, prow + 1], [bcols[idx] - 1] * 2
        for c in range(pcol + 2, bcols[idx]):
          if not put(output, prow, c, pcolor): return None, None
      if prow >= brows[idx] + talls[idx]:
        rows, cols = [brows[idx] + talls[idx]] * 2, [pcol - 1, pcol + 1]
        for r in range(brows[idx] + talls[idx], prow - 1):
          if not put(output, r, pcol, pcolor): return None, None
      if prow < brows[idx]:
        rows, cols = [brows[idx] - 1] * 2, [pcol - 1, pcol + 1]
        for r in range(prow + 2, brows[idx]):
          if not put(output, r, pcol, pcolor): return None, None
      for row, col in zip(rows, cols):
        if not put(output, row, col, pcolor): return None, None
    return grid, output

  if width is None:
    width, height = common.randint(12, 30), common.randint(12, 30)
    num_boxes = 1
    if width * height >= 250: num_boxes = common.randint(1, 2)
    if width * height >= 500: num_boxes = common.randint(2, 3)
    bgcolor = common.random_color()
    bcolors = common.random_colors(num_boxes, exclude=[bgcolor])
    while True:
      cdirs = [common.randint(0, 1) for _ in range(num_boxes)]
      wides = [common.randint(2, 4) if d else common.randint(7, min(11, width - 4)) for d in cdirs]
      talls = [common.randint(7, min(11, height - 4)) if d else common.randint(2, 4) for d in cdirs]
      brows = [common.randint(2, height - tall - 2) for tall in talls]
      bcols = [common.randint(2, width - wide - 2) for wide in wides]
      prows, pcols, pcolors = [], [], []
      for cdir, wide, tall, brow, bcol, bcolor in zip(cdirs, wides, talls, brows, bcols, bcolors):
        num_pixels = common.randint(1, 3)
        if cdir:
          prows.extend(common.sample(list(range(brow + 1, brow + tall - 1)), num_pixels))
          pcols.extend(common.sample(list(range(1, bcol - 2)) + list(range(bcol + wide + 2, width - 1)), num_pixels))
        else:
          prows.extend(common.sample(list(range(1, brow - 2)) + list(range(brow + tall + 2, height - 1)), num_pixels))
          pcols.extend(common.sample(list(range(bcol + 1, bcol + wide - 1)), num_pixels))
        pcolors.extend([bcolor] * num_pixels)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=22, bgcolor=3, wides=[3, 3], talls=[8, 7],
               brows=[2, 11], bcols=[4, 8], bcolors=[1, 4], prows=[3, 12, 15],
               pcols=[12, 13, 3], pcolors=[1, 4, 4]),
      generate(width=16, height=13, bgcolor=8, wides=[7], talls=[2], brows=[4],
               bcols=[3], bcolors=[3], prows=[1, 9], pcols=[7, 5],
               pcolors=[3, 3]),
      generate(width=16, height=22, bgcolor=1, wides=[11], talls=[3], brows=[8],
               bcols=[2], bcolors=[8], prows=[2, 3, 17], pcols=[9, 5, 8],
               pcolors=[8, 8, 8]),
  ]
  test = [
      generate(width=30, height=30, bgcolor=4, wides=[4, 3, 10],
               talls=[7, 7, 3], brows=[2, 11, 23], bcols=[10, 15, 4],
               bcolors=[2, 1, 3], prows=[3, 5, 13, 16, 19],
               pcols=[23, 4, 5, 26, 7], pcolors=[2, 2, 1, 1, 3]),
  ]
  return {"train": train, "test": test}
