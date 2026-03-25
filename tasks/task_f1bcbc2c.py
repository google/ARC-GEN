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


def generate(flop=None, col=None, pos=None, lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    flop: Whether to flop the grid horizontally.
    col: The column to start drawing from.
    pos: The position of the maroon pixel.
    lengths: The lengths of the segments.
  """

  def draw():
    grid, output = common.grids(10, 10)
    r, c, rdir, cdir, i, color, transparent = 0, col, 0, 1, 0, 8, -2
    for length in lengths:
      rdir, cdir = 1 - rdir, 1 - cdir
      for _ in range(length - 1):
        if r < 0 or r >= 10 or c < 0 or c >= 10: return None, None
        if (c == 9 and rdir) or (r == 9 and cdir): return None, None
        grid[r][c] = 9 if i == pos else transparent
        output[r][c] = color if output[r][c] != 9 else 9
        r, c, i = r + rdir, c + cdir, i + 1
      if i == pos:
        if rdir == 0: return None, None  # Wrong kind of turn.
        output[r][c] = 9
        color = transparent
    if r < 0 or r >= 10 or c < 0 or c >= 10: return None, None
    grid[r][c] = transparent
    output[r][c] = color
    r, c = r + rdir, c + cdir
    if not (r < 0 or r >= 10 or c < 0 or c >= 10): return None, None
    # Draw the orange borders.
    for r in range(10):
      for c in range(10):
        if common.get_pixel(grid, r, c) != 0: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(grid, r + dr, c + dc) in [transparent, 9]:
              output[r][c] = grid[r][c] = 7
    # Change all the transparent pixels to black.
    for r in range(10):
      for c in range(10):
        if grid[r][c] == transparent: grid[r][c] = 0
        if output[r][c] == transparent: output[r][c] = 0
    if flop: grid, output = common.flop(grid), common.flop(output)
    return grid, output

  if flop is None:
    flop = common.randint(0, 1)
    col = common.randint(1, 4)
    pos = -1 if common.randint(0, 1) else common.randint(6, 9)
    while True:
      lengths = [common.randint(3, 7) for _ in range(common.randint(3, 5))]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(flop=1, col=3, pos=9, lengths=[4, 3, 7]),
      generate(flop=0, col=1, pos=9, lengths=[4, 4, 4, 4, 4]),
      generate(flop=0, col=3, pos=6, lengths=[4, 3, 5, 3, 3]),
      generate(flop=0, col=4, pos=-1, lengths=[4, 3, 6, 4]),
  ]
  test = [
      generate(flop=1, col=1, pos=9, lengths=[4, 4, 4, 5, 4]),
  ]
  return {"train": train, "test": test}
