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


def generate(width=None, height=None, prows=None, pcols=None, plengths=None,
             pcolors=None, cdirs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    plengths: The lengths of the pixels.
    pcolors: The colors of the pixels.
    cdirs: The directions of the lines.
  """

  def draw():
    grid, output = common.grids(width, height)
    counts = common.grid(width, height)
    overlaps = 0
    for the_dir in [0, 1]:
      for prow, pcol, plength, pcolor, cdir in zip(prows, pcols, plengths,
                                                   pcolors, cdirs):
        if cdir != the_dir: continue
        row, col = prow, pcol
        grid[row][col] = pcolor
        if cdir: row = prow + plength - 1
        else: col = pcol + plength - 1
        grid[row][col] = pcolor
        for i in range(plength):
          row = (prow + i) if cdir else prow
          col = pcol if cdir else (pcol + i)
          if output[row][col] != 0: overlaps += 1
          output[row][col] = pcolor
          counts[row][col] += 1
    # Some additional checks.
    for prow, pcol, plength, cdir in zip(prows, pcols, plengths, cdirs):
      row, col = prow, pcol
      # First, make sure the endpoints occupy coordinates by themselves.
      if counts[row][col] > 1: return None, None, None
      if cdir: row = prow + plength - 1
      else: col = pcol + plength - 1
      if counts[row][col] > 1: return None, None, None
      # Second, make sure the lines don't run into others.
      if cdir: row = prow - 1
      else: col = pcol - 1
      if output[row][col] != 0: return None, None, None
      if cdir: row = prow + plength
      else: col = pcol + plength
      if output[row][col] != 0: return None, None, None
    return grid, output, overlaps

  if width is None:
    while True:
      width, height = 10 * common.randint(1, 3), 10 * common.randint(1, 3)
      if abs(width - height) <= 10: break
    pcolors, expected_overlaps = common.random_colors(5), common.randint(2, 3)
    while True:
      cdirs = [common.randint(0, 1) for _ in range(5)]
      if sum(cdirs) in [2, 3]: break
    while True:
      plengths = [common.randint(4, (height - 2) if cdir else (width - 2)) for cdir in cdirs]
      prows = [common.randint(1, height - 1 - (plength if cdir else 1)) for cdir, plength in zip(cdirs, plengths)]
      pcols = [common.randint(1, width - 1 - (1 if cdir else plength)) for cdir, plength in zip(cdirs, plengths)]
      grid, _, overlaps = draw()
      if grid is not None and overlaps == expected_overlaps: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=20, prows=[2, 4, 8, 12, 14],
               pcols=[3, 2, 2, 5, 1], plengths=[9, 6, 4, 7, 6],
               pcolors=[4, 3, 7, 9, 8], cdirs=[1, 0, 0, 1, 0]),
      generate(width=20, height=30, prows=[2, 6, 12, 18, 20],
               pcols=[6, 3, 14, 4, 2], plengths=[12, 9, 6, 10, 6],
               pcolors=[2, 3, 8, 6, 5], cdirs=[1, 0, 1, 1, 0]),
  ]
  test = [
      generate(width=20, height=20, prows=[1, 2, 3, 7, 14],
               pcols=[3, 9, 1, 7, 8], plengths=[18, 8, 16, 7, 7],
               pcolors=[3, 5, 2, 7, 8], cdirs=[1, 1, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
