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


def generate(rows=None, cols=None, lengths=None, cdirs=None, pcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: rows of the lines.
    cols: columns of the lines.
    lengths: lengths of the lines.
    cdirs: directions of the lines.
    pcol: col of the pixel.
  """

  def draw():
    nonlocal pcol
    grid, output = common.grids(10, 10)

    def check_for_holes(row, col):
      holes = []
      for c in range(col, 10):  # Check for a wall to the right.
        if grid[row][c] == 2: break  # We see a wall, so it's closed!
        if grid[row + 1][c] == 0: holes.append(c)
      for c in range(col, -1, -1):  # Check for a wall to the left
        if grid[row][c] == 2: break  # We see a wall, so it's closed!
        if grid[row + 1][c] == 0: holes.append(c)
      return holes

    def fill(row, col):
      while True:
        if sum([grid[row][c] for c in range(10)]) == 0: break
        for c in range(col, 10):
          if output[row][c] == 2: break
          output[row][c] = 1
        for c in range(col, -1, -1):
          if output[row][c] == 2: break
          output[row][c] = 1
        row -= 1

    # First, draw the red lines.
    for row, col, length, cdir in zip(rows, cols, lengths, cdirs):
      for i in range(length):
        r, c = row + (i if cdir else 0), col + (0 if cdir else i)
        output[r][c] = grid[r][c] = 2
    # Then, draw the blue dot.
    prow = 0
    grid[prow][pcol] = 1
    # Then, the dot trickles down, and we check various conditions.
    while prow < 9:
      if grid[prow + 1][pcol] == 2:
        holes = check_for_holes(prow, pcol)
        if not holes:
          fill(prow, pcol)
          break
        if len(holes) == 1:
          pcol = holes[0]
        else: return None, None  # Ill-defined case.
      prow += 1
    # If we made it all the way down, draw the thin puddle of water.
    if prow == 9:
      for c in range(10):
        output[9][c] = 1
    return grid, output

  if rows is None:
    while True:
      # First, choose the locations of all vertical lines.
      if common.randint(0, 1):  # the single case
        vrows, vcols, vlengths = [3, 3], [2, 7], [4, 4]
        middle = common.randint(0, 2)
        if middle:
          vrows.append(3)
          vcols.append(3 + middle)
          vlengths.append(4)
      else:  # the double case
        vrows, vcols, vlengths = [2, 2, 6, 6], [], [3, 3, 3, 3]
        for _ in range(2):  # For the top and bottom boxes.
          while True:
            cols = sorted(common.sample(range(10), 2))
            if cols[0] + 1 < cols[1]: break
          vcols.extend(cols)
      # Second, extend the bottom of those lines to the left, right, or neither.
      hrows, hcols, hlengths = [], [], []
      for vrow, vcol, vlength in zip(vrows, vcols, vlengths):
        col = max(vcol - common.randint(0, 3), 2)
        if col < vcol:
          hrows.append(vrow + vlength - 1)
          hcols.append(col)
          hlengths.append(vcol - col)
        col = min(vcol + common.randint(0, 3), 8)
        if col > vcol:
          hrows.append(vrow + vlength - 1)
          hcols.append(vcol)
          hlengths.append(col - vcol)
      rows = vrows + hrows
      cols = vcols + hcols
      lengths = vlengths + hlengths
      cdirs = [1] * len(vlengths) + [0] * len(hlengths)
      pcol = common.randint(1, 8)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3, 3, 3, 6], cols=[2, 5, 7, 2], lengths=[4, 4, 4, 4], cdirs=[1, 1, 1, 0], pcol=4),
      generate(rows=[3, 3, 6], cols=[2, 7, 2], lengths=[4, 4, 6], cdirs=[1, 1, 0], pcol=8),
      generate(rows=[3, 3, 6], cols=[2, 7, 2], lengths=[4, 4, 4], cdirs=[1, 1, 0], pcol=4),
      generate(rows=[3, 3, 3, 6], cols=[2, 5, 7, 4], lengths=[4, 4, 4, 4], cdirs=[1, 1, 1, 0], pcol=6),
      generate(rows=[3, 3, 6], cols=[2, 7, 2], lengths=[4, 4, 6], cdirs=[1, 1, 0], pcol=6),
  ]
  test = [
      generate(rows=[2, 2, 4, 6, 6, 8], cols=[5, 9, 7, 2, 8, 2], lengths=[3, 3, 3, 3, 3, 7], cdirs=[1, 1, 0, 1, 1, 0], pcol=8),
  ]
  return {"train": train, "test": test}
