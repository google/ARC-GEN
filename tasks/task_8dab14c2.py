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


def generate(width=None, height=None, length=None, depth=None, flip=None,
             flop=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    length: The length of the L shape.
    depth: The depth of the L shape.
    flip: Whether to flip the grids horizontally.
    flop: Whether to flop the grids vertically.
    prows: The rows of the points.
    pcols: The columns of the points.
  """

  def draw():
    if prows is None or pcols is None: return None, None
    pixels = list(zip(prows, pcols))
    if len(set(pixels)) != len(pixels): return None, None  # Duplicate pixels.
    grid, output = common.grids(width, height, 8)
    rowlist, collist = [], []
    def fill(r, c, rdir, cdir):
      i = 1
      while grid[r + i * rdir][c + i * cdir] == 1:
        i += 1
      if grid[r][c] == 8: i -= 1
      output[r + i * rdir][c + i * cdir] = output[r][c]
    # Draw the blue L.
    for g in [grid, output]:
      common.rect(g, length, height - 4, 2, 2, 1)
      common.rect(g, width - 4, depth, 2, 2, 1)
    # Draw the new points.
    for prow, pcol in zip(prows, pcols):
      rdir, cdir = 0, 0
      if grid[prow][pcol] == 1:
        if grid[prow][pcol - 1] == 8: cdir = 1
        if grid[prow][pcol + 1] == 8: cdir = -1
        if grid[prow - 1][pcol] == 8: rdir = 1
        if grid[prow + 1][pcol] == 8: rdir = -1
      else:
        if grid[prow][pcol - 1] == 1: cdir = -1
        if grid[prow][pcol + 1] == 1: cdir = 1
        if grid[prow - 1][pcol] == 1: rdir = -1
        if grid[prow + 1][pcol] == 1: rdir = 1
      fill(prow, pcol, rdir, cdir)
      if rdir != 0:
        if pcol in collist: return None, None
        collist.append(pcol)
      if cdir != 0:
        if prow in rowlist: return None, None
        rowlist.append(prow)
    # Draw the old points.
    for prow, pcol in zip(prows, pcols):
      grid[prow][pcol] = 1 if grid[prow][pcol] == 8 else 8
      output[prow][pcol] = 1 if output[prow][pcol] == 8 else 8
    # Make sure that we preserve all corners of the L (since their effect would
    # be undefined).
    if grid[2][2] == 8: return None, None
    if grid[2][width - 3] == 8: return None, None
    if grid[depth + 1][width - 3] == 8: return None, None
    if grid[height - 3][2] == 8: return None, None
    if grid[height - 3][length + 1] == 8: return None, None
    # Make sure the inner corner of the L is empty (again, otherwise undefined).
    if grid[depth + 2][length + 2] == 1: return None, None
    # Make sure all blue (or cyan) pixels are connected.
    for color in [1, 8]:
      pixels = []
      for r in range(height):
        for c in range(width):
          if output[r][c] == color: pixels.append((r, c))
      if not common.connected(pixels): return None, None
    # Flip and flop!
    if flip: grid, output = common.flip(grid), common.flip(output)
    if flop: grid, output = common.flop(grid), common.flop(output)
    return grid, output

  if width is None:
    width, height = common.randint(12, 18), common.randint(12, 18)
    length, depth = common.randint(3, 6), common.randint(3, 6)
    flip, flop = common.randint(0, 1), common.randint(0, 1)
    ub = 7
    while True:
      prows, pcols = [], []
      for row in range(2, height - 2):  # Left of L
        if common.randint(0, ub): continue
        prows.append(row)
        pcols.append(common.randint(1, 2))
      for col in range(2, width - 2):  # Bottom of L
        if common.randint(0, ub): continue
        pcols.append(col)
        prows.append(common.randint(1, 2))
      for row in range(2, depth + 2):  # Right of L
        if common.randint(0, ub): continue
        prows.append(row)
        pcols.append(width - common.randint(2, 3))
      for col in range(length + 2, width - 2):  # Shelf of L
        if common.randint(0, ub): continue
        pcols.append(col)
        prows.append(depth + common.randint(1, 2))
      for row in range(depth + 2, height - 2):  # Wall of L
        if common.randint(0, ub): continue
        prows.append(row)
        pcols.append(length + common.randint(1, 2))
      for col in range(2, length + 2):  # Top of L
        if common.randint(0, ub): continue
        pcols.append(col)
        prows.append(height - common.randint(2, 3))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=14, length=3, depth=5, flip=0, flop=1,
               prows=[10, 7, 4, 2], pcols=[2, 10, 13, 5]),
      generate(width=17, height=13, length=4, depth=3, flip=0, flop=0,
               prows=[9, 7, 4, 2, 1, 1], pcols=[5, 1, 2, 1, 6, 12]),
      generate(width=16, height=16, length=4, depth=3, flip=1, flop=0,
               prows=[14, 4], pcols=[5, 11]),
      generate(width=15, height=14, length=4, depth=5, flip=1, flop=1,
               prows=[12, 4], pcols=[3, 12]),
  ]
  test = [
      generate(width=16, height=16, length=3, depth=5, flip=0, flop=1,
               prows=[11, 6, 6, 2], pcols=[4, 2, 10, 5]),
      generate(width=16, height=16, length=3, depth=3, flip=0, flop=0,
               prows=[8, 5, 5], pcols=[1, 6, 10]),
      generate(width=16, height=16, length=6, depth=4, flip=1, flop=1,
               prows=[14, 5, 4, 2, 2, 1], pcols=[7, 14, 2, 1, 6, 2]),
      generate(width=16, height=16, length=3, depth=5, flip=1, flop=0,
               prows=[4, 1], pcols=[13, 3]),
  ]
  return {"train": train, "test": test}
