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


def generate(width=None, height=None, bgcolor=None, fgcolor=None, prows=None,
             pcols=None, pcolors=None, pdirs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    bgcolor: The background color of the grids.
    fgcolor: The foreground color of the grids.
    prows: The rows of the sprites.
    pcols: The columns of the sprites.
    pcolors: The colors of the sprites.
    pdirs: The directions of the sprites.
  """

  def draw():
    if common.overlaps(prows, pcols, [6] * len(prows), [6] * len(pcols)):
      return None, None  # Too close.
    if len(set(pdirs)) != len(pdirs):
      return None, None  # Duplicate directions.
    grid, output = common.grids(width, height, bgcolor)
    drs = {0: [0, 0, 0, 0, 1, 1, 1],
           1: [-2, -1, -1, 0, 1, 1, 2],
           2: [-1, -1, -1, 0, 0, 0, 0],
           3: [-2, -1, -1, 0, 1, 1, 2]}
    dcs = {0: [-2, -1, 1, 2, -1, 0, 1],
           1: [0, -1, 0, -1, -1, 0, 0],
           2: [-1, 0, 1, -2, -1, 1, 2],
           3: [0, 0, 1, 1, 0, 1, 0]}
    rdirs, cdirs = [-1, 0, 1, 0], [0, 1, 0, -1]
    # Draw the sprites, their laser beams, and walls.
    for prow, pcol, pcolor, pdir in zip(prows, pcols, pcolors, pdirs):
      for dr, dc in zip(drs[pdir], dcs[pdir]):
        r, c = prow + dr, pcol + dc
        if r < 1 or r >= height - 1 or c < 1 or c >= width - 1:
          return None, None
        if output[r][c] != bgcolor: return None, None
        output[r][c] = grid[r][c] = fgcolor
      if output[prow][pcol] != bgcolor: return None, None
      output[prow][pcol] = grid[prow][pcol] = pcolor
      dist = 0  # We color every other cell -1 to detect collisions.
      while True:
        prow, pcol = prow + rdirs[pdir], pcol + cdirs[pdir]
        if prow < 0 or prow >= height or pcol < 0 or pcol >= width:
          break
        if output[prow][pcol] != bgcolor: return None, None
        output[prow][pcol] = pcolor if dist % 2 else -1
        dist += 1
      if pdir in [0, 2]:
        r = 0 if pdir == 0 else (height - 1)
        for c in range(width):
          output[r][c] = pcolor if output[r][c] in [bgcolor, pcolor, -1] else 0
      else:
        c = 0 if pdir == 3 else (width - 1)
        for r in range(height):
          output[r][c] = pcolor if output[r][c] in [bgcolor, pcolor, -1] else 0
    # Change the -1's back to the background color.
    for row in range(height):
      for col in range(width):
        if output[row][col] == -1: output[row][col] = bgcolor
    return grid, output

  if width is None:
    width, height = common.randint(10, 18), common.randint(10, 18)
    num_sprites = common.randint(1, 2)
    if width * height >= 200: num_sprites += 1
    colors = common.shuffle(list(range(1, 10)))
    bgcolor = colors.pop()
    fgcolor = colors.pop()
    pcolors = [colors.pop() for _ in range(num_sprites)]
    while True:
      prows = [common.randint(2, height - 3) for _ in range(num_sprites)]
      pcols = [common.randint(2, width - 3) for _ in range(num_sprites)]
      pdirs = [common.randint(0, 3) for _ in range(num_sprites)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, bgcolor=2, fgcolor=4, prows=[3, 8],
               pcols=[9, 2], pcolors=[1, 8], pdirs=[0, 1]),
      generate(width=13, height=11, bgcolor=1, fgcolor=8, prows=[3, 5],
               pcols=[9, 3], pcolors=[3, 2], pdirs=[0, 3]),
      generate(width=12, height=15, bgcolor=3, fgcolor=1, prows=[2], pcols=[5],
               pcolors=[6], pdirs=[2]),
  ]
  test = [
      generate(width=17, height=15, bgcolor=4, fgcolor=2, prows=[3, 5, 11],
               pcols=[2, 12, 7], pcolors=[1, 5, 8], pdirs=[3, 1, 0]),
  ]
  return {"train": train, "test": test}
