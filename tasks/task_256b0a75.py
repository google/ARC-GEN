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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, bcolor=None, bangle=None, prows=None, pcols=None,
             pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw(enforce=True):
    grid, output = common.grids(width, height)
    for g in [grid]:
      g[brow][bcol] = g[brow + 1][bcol] = g[brow][bcol + 1] = 8 if bangle != 0 else bcolor
      g[brow][bcol + wide - 1] = g[brow + 1][bcol + wide - 1] = g[brow][bcol + wide - 2] = 8 if bangle != 1 else bcolor
      g[brow + tall - 1][bcol] = g[brow + tall - 2][bcol] = g[brow + tall - 1][bcol + 1] = 8 if bangle != 2 else bcolor
      g[brow + tall - 1][bcol + wide - 1] = g[brow + tall - 2][bcol + wide - 1] = g[brow + tall - 1][bcol + wide - 2] = 8 if bangle != 3 else bcolor
    common.rect(output, width, tall, brow, 0, bcolor)
    common.rect(output, wide, height, 0, bcol, bcolor)
    common.hollow_rect(output, wide, tall, brow, bcol, 8)
    for prow, pcol, pcolor in zip(prows, pcols, pcolors):
      output[prow][pcol] = grid[prow][pcol] = pcolor
      if brow <= prow < brow + tall and pcol < bcol:
        for c in range(pcol - 1, -1, -1):
          if grid[prow][c] == bcolor and enforce: return None, None
          if grid[prow][c] != 0: break
          output[prow][c] = pcolor
      elif brow <= prow < brow + tall and pcol >= bcol + wide:
        for c in range(pcol + 1, width):
          if grid[prow][c] == bcolor and enforce: return None, None
          if grid[prow][c] != 0: break
          output[prow][c] = pcolor
      elif bcol <= pcol < bcol + wide and prow < brow:
        for r in range(prow - 1, -1, -1):
          if grid[r][pcol] == bcolor and enforce: return None, None
          if grid[r][pcol] != 0: break
          output[r][pcol] = pcolor
      elif bcol <= pcol < bcol + wide and prow >= brow + tall:
        for r in range(prow + 1, height):
          if grid[r][pcol] == bcolor and enforce: return None, None
          if grid[r][pcol] != 0: break
          output[r][pcol] = pcolor
      else:
        output[prow][pcol] = pcolor
    return grid, output

  if width is None:
    base = common.randint(21, 25)
    width, height = base + common.randint(-1, 1), base + common.randint(-1, 1)
    wide, tall = common.randint(5, 10), common.randint(5, 10)
    brow = common.randint(3, height - tall - 3)
    bcol = common.randint(3, width - wide - 3)
    bcolor = common.random_color(exclude=[8])
    bangle = common.randint(0, 3)
    while True:
      grid = common.grid(width, height)
      for g in [grid]:
        g[brow][bcol] = g[brow + 1][bcol] = g[brow][bcol + 1] = 8 if bangle != 0 else bcolor
        g[brow][bcol + wide - 1] = g[brow + 1][bcol + wide - 1] = g[brow][bcol + wide - 2] = 8 if bangle != 1 else bcolor
        g[brow + tall - 1][bcol] = g[brow + tall - 2][bcol] = g[brow + tall - 1][bcol + 1] = 8 if bangle != 2 else bcolor
        g[brow + tall - 1][bcol + wide - 1] = g[brow + tall - 2][bcol + wide - 1] = g[brow + tall - 1][bcol + wide - 2] = 8 if bangle != 3 else bcolor
        prows, pcols, pcolors = [], [], []
      for r in range(height):
        for c in range(width):
          if brow <= r < brow + tall and bcol <= c < bcol + wide: continue
          if common.randint(0, 19): continue
          good = True
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if common.get_pixel(grid, nr, nc) not in [-1, 0]: good = False
          if not good: continue
          prows.append(r)
          pcols.append(c)
          pcolors.append(common.random_color(exclude=[8]))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=24, height=22, wide=7, tall=8, brow=4, bcol=10, bcolor=1,
               bangle=0,
               prows=[0, 0, 0, 0, 0, 1, 2, 3, 3, 7, 8, 10, 11, 12, 13, 14, 15, 17, 17, 18, 20, 21, 21],
               pcols=[1, 7, 12, 19, 22, 10, 6, 1, 4, 23, 19, 6, 20, 3, 16, 19, 13, 5, 10, 23, 13, 15, 23],
               pcolors=[4, 4, 6, 1, 5, 4, 7, 2, 9, 2, 1, 2, 7, 9, 7, 5, 1, 5, 3, 1, 3, 1, 4]),
      generate(width=21, height=23, wide=6, tall=8, brow=7, bcol=9, bcolor=7,
               bangle=2, prows=[1, 3, 3, 7, 9, 11, 13, 17, 20, 21],
               pcols=[13, 3, 10, 2, 17, 4, 18, 13, 3, 18],
               pcolors=[4, 3, 6, 2, 7, 4, 9, 1, 1, 9]),
      generate(width=23, height=23, wide=8, tall=10, brow=6, bcol=6, bcolor=3,
               bangle=3,
               prows=[0, 0, 1, 3, 3, 5, 6, 8, 10, 14, 15, 15, 18, 19, 19, 20, 22],
               pcols=[9, 11, 15, 6, 10, 11, 19, 3, 1, 2, 1, 18, 12, 1, 2, 11, 8],
               pcolors=[7, 5, 9, 1, 9, 6, 6, 5, 6, 1, 6, 1, 1, 5, 2, 9, 1]),
  ]
  test = [
      generate(width=26, height=25, wide=9, tall=7, brow=9, bcol=6, bcolor=6,
               bangle=1,
               prows=[0, 0, 0, 1, 1, 3, 4, 5, 7, 8, 8, 10, 11, 11, 16, 19, 20, 20, 21, 22],
               pcols=[0, 8, 15, 16, 24, 4, 21, 12, 6, 10, 16, 18, 3, 19, 9, 15, 2, 7, 17, 22],
               pcolors=[7, 9, 3, 2, 6, 9, 1, 4, 2, 7, 9, 9, 3, 7, 4, 2, 1, 5, 7, 9])
  ]
  return {"train": train, "test": test}
