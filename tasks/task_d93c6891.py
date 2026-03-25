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


def generate(width=None, height=None, ywidth=None, yheight=None, yrow=None,
             ycol=None, offsets=None, wides=None, talls=None, lefts=None,
             rights=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: Width of the grids.
    height: Height of the grids.
    ywidth: Width of the yellow rectangle.
    yheight: Height of the yellow rectangle.
    yrow: Row of the yellow rectangle.
    ycol: Column of the yellow rectangle.
    offsets: Offsets of the inner rectangles.
    wides: Widths of the inner rectangles.
    talls: Heights of the inner rectangles.
    lefts: Left sides of the inner rectangles.
    rights: Rights sides of the inner rectangles.
  """

  def draw():
    if ywidth * yheight + 1 < width * height // 2 - 1: return None, None
    grid, output = common.grids(width, height)
    ids = common.grid(width, height, -1)
    def next_left(r, c):
      if r == 0 and c + 1 < ywidth: return r, c + 1
      if r == 0 and c + 1 == ywidth: return r + 1, c
      if c + 1 == ywidth and r + 1 < yheight: return r + 1, c
      if c + 1 == ywidth and r + 1 == yheight: return r, c - 1
      if r + 1 == yheight and c > 0: return r, c - 1
      if r + 1 == yheight and c == 0: return r - 1, c
      if c == 0 and r > 0: return r - 1, c
      if c == 0 and r == 0: return r, c + 1
      return -1, -1
    def next_right(r, c):
      if r == 0 and c > 0: return r, c - 1
      if r == 0 and c == 0: return r + 1, c
      if c == 0 and r + 1 < yheight: return r + 1, c
      if c == 0 and r + 1 == yheight: return r, c + 1
      if r + 1 == yheight and c + 1 < ywidth: return r, c + 1
      if r + 1 == yheight and c + 1 == ywidth: return r - 1, c
      if c + 1 == ywidth and r > 0: return r - 1, c
      if c + 1 == ywidth and r == 0: return r, c - 1
      return -1, -1
    def draw_left(i, r, c, left):
      for _ in range(left):
        if grid[yrow + r][ycol + c] != 4: return False
        grid[yrow + r][ycol + c] = 5
        ids[yrow + r][ycol + c] = i
        r, c = next_left(r, c)
      if grid[yrow + r][ycol + c] != 4: return False
      return True
    def draw_right(i, r, c, right):
      for _ in range(right):
        if grid[yrow + r][ycol + c] != 4: return False
        grid[yrow + r][ycol + c] = 5
        ids[yrow + r][ycol + c] = i
        r, c = next_right(r, c)
      if grid[yrow + r][ycol + c] != 4: return False
      return True
    common.rect(grid, ywidth, yheight, yrow, ycol, 4)
    common.rect(output, ywidth, yheight, yrow, ycol, 4)
    for i in range(4):
      offset, wide, tall = offsets[i], wides[i], talls[i]
      left, right = lefts[i], rights[i]
      gtall = (left + right) // wide
      if offset == -1: continue
      if i == 0:
        common.rect(ids, wide, tall, yrow, ycol + offset, i)
        common.rect(grid, wide, tall, yrow, ycol + offset, 7)
        common.rect(output, wide, tall, yrow, ycol + offset, 7)
        common.rect(output, wide, gtall, yrow, ycol + offset, 5)
        if not draw_left(i, 0, offset + wide, left): return None, None
        if not draw_right(i, 0, offset - 1, right): return None, None
      if i == 1:
        common.rect(ids, tall, wide, yrow + offset, ycol + ywidth - tall, i)
        common.rect(grid, tall, wide, yrow + offset, ycol + ywidth - tall, 7)
        common.rect(output, tall, wide, yrow + offset, ycol + ywidth - tall, 7)
        common.rect(output, gtall, wide, yrow + offset, ycol + ywidth - gtall, 5)
        if not draw_left(i, offset + wide, ywidth - 1, left): return None, None
        if not draw_right(i, offset - 1, ywidth - 1, right): return None, None
      if i == 2:
        common.rect(ids, wide, tall, yrow + yheight - tall, ycol + ywidth - wide - offset, i)
        common.rect(grid, wide, tall, yrow + yheight - tall, ycol + ywidth - wide - offset, 7)
        common.rect(output, wide, tall, yrow + yheight - tall, ycol + ywidth - wide - offset, 7)
        common.rect(output, wide, gtall, yrow + yheight - gtall, ycol + ywidth - wide - offset, 5)
        if not draw_left(i, yheight - 1, ywidth - wide - offset - 1, left): return None, None
        if not draw_right(i, yheight - 1, ywidth - offset, right): return None, None
      if i == 3:
        common.rect(ids, tall, wide, yrow + yheight - wide - offset, ycol, i)
        common.rect(grid, tall, wide, yrow + yheight - wide - offset, ycol, 7)
        common.rect(output, tall, wide, yrow + yheight - wide - offset, ycol, 7)
        common.rect(output, gtall, wide, yrow + yheight - wide - offset, ycol, 5)
        if not draw_left(i, yheight - wide - offset - 1, 0, left): return None, None
        if not draw_right(i, yheight - offset, 0, right): return None, None
    # Check that rectangles don't touch.
    for row in range(height):
      for col in range(width):
        if ids[row][col] == -1: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
              if ids[nr][nc] != -1 and ids[nr][nc] != ids[row][col]:
                return None, None
    if 5 not in common.flatten(grid) or 7 not in common.flatten(grid):
      return None, None
    return grid, output

  if width is None:
    while True:
      width = 2 * common.randint(4, 9)
      height = 2 * common.randint(4, 9)
      ywidth = max(common.randint(width // 2, width), 8)
      yheight = max(common.randint(height // 2, height), 8)
      yrow = common.randint(0, height - yheight)
      ycol = common.randint(0, width - ywidth)
      offsets, wides, talls, lefts, rights = [], [], [], [], []
      def add_nulls():
        offsets.append(-1)
        wides.append(-1)
        talls.append(-1)
        lefts.append(-1)
        rights.append(-1)
      for _ in range(2):
        if ywidth < 8:
          add_nulls()
        else:
          wides.append(common.randint(2, 6))
          talls.append(common.randint(0, 6))
          offsets.append(common.randint(1, ywidth - wides[-1] - 1))
          gtall = common.randint(0, talls[-1])
          lefts.append(common.randint(0, gtall * wides[-1]))
          rights.append(gtall * wides[-1] - lefts[-1])
        if yheight < 8:
          add_nulls()
        else:
          wides.append(common.randint(2, 6))
          talls.append(common.randint(0, 6))
          offsets.append(common.randint(1, yheight - wides[-1] - 1))
          gtall = common.randint(0, talls[-1])
          lefts.append(common.randint(0, gtall * wides[-1]))
          rights.append(gtall * wides[-1] - lefts[-1])
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=16, ywidth=12, yheight=12, yrow=4, ycol=4,
               offsets=[5, -1, -1, 3], wides=[3, -1, -1, 3],
               talls=[2, -1, -1, 3], lefts=[3, -1, -1, 6],
               rights=[3, -1, -1, 0]),
      generate(width=14, height=10, ywidth=14, yheight=6, yrow=0, ycol=0,
               offsets=[-1, -1, 7, -1], wides=[-1, -1, 3, -1],
               talls=[-1, -1, 2, -1], lefts=[-1, -1, 2, -1],
               rights=[-1, -1, 4, -1]),
      generate(width=16, height=16, ywidth=14, yheight=9, yrow=4, ycol=0,
               offsets=[3, 6, 8, -1], wides=[6, 2, 4, -1], talls=[2, 2, 1, -1],
               lefts=[3, 4, 0, -1], rights=[3, 0, 0, -1]),

  ]
  test = [
      generate(width=18, height=16, ywidth=15, yheight=13, yrow=1, ycol=1,
               offsets=[3, 4, 5, 4], wides=[2, 2, 4, 2], talls=[5, 6, 3, 3],
               lefts=[7, 5, 5, 0], rights=[3, 1, 3, 0]),
  ]
  return {"train": train, "test": test}
