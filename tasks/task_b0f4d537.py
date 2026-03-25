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


def generate(height=None, cdirs=None, ivals=None, ovals=None, colors=None,
             flop=None, erows=None, ecols=None, ecolors=None, egrids=None):
  """Returns input and output grids according to the given parameters.

  Args:
    height: height of the black grid.
    cdirs: directions of the lines.
    ivals: input vals of the lines.
    ovals: output vals of the lines.
    colors: colors of the lines.
    flop: whether to flop the grid.
    erows: rows of the extra pixels.
    ecols: columns of the extra pixels.
    ecolors: colors of the extra pixels.
    egrids: grids of the extra pixels.
  """

  width = 7
  if height is None:
    height = common.randint(6, 12)
    while True:
      verts = common.randint(1, 3)
      horizs = common.randint(1, 2)
      if verts + horizs < 3: continue
      vspaces = [common.randint(1, 4) for _ in range(horizs + 1)]
      hspaces = [common.randint(1, 4) for _ in range(verts + 1)]
      if sum(vspaces) + horizs != height or sum(hspaces) + verts != width: continue
      break
    raw_colors = common.shuffle([1, 2, 3])
    if horizs == 1:
      hcolors, vcolors = [raw_colors[0], raw_colors[1]], [raw_colors[2]]
    elif verts == 1:
      hcolors, vcolors = [raw_colors[0]], [raw_colors[1], raw_colors[2]]
    elif common.randint(0, 1):
      hcolors, vcolors = [raw_colors[0], raw_colors[1]], [raw_colors[2]]
    else:
      hcolors, vcolors = [raw_colors[0]], [raw_colors[1], raw_colors[2]]
    cdirs, ivals, ovals, colors = [], [], [], []
    row = 0
    vspaces.pop()
    for i, vspace in enumerate(vspaces):
      row += vspace
      cdirs.append(0)
      ivals.append(2 * i + 1)
      ovals.append(row)
      colors.append(vcolors[i % len(vcolors)])
      row += 1
    col = 0
    hspaces.pop()
    for i, hspace in enumerate(hspaces):
      col += hspace
      cdirs.append(1)
      ivals.append(2 * i + 1)
      ovals.append(col)
      colors.append(hcolors[i % len(hcolors)])
      col += 1
    indexs = common.shuffle(list(range(len(cdirs))))
    cdirs = [cdirs[i] for i in indexs]
    ivals = [ivals[i] for i in indexs]
    ovals = [ovals[i] for i in indexs]
    colors = [colors[i] for i in indexs]
    flop = common.randint(0, 1)

  verts = sum([1 if cdir == 1 else 0 for cdir in cdirs])
  horizs = sum([1 if cdir == 0 else 0 for cdir in cdirs])
  grid = common.grid(width + 2 * verts + 2, height)
  output = common.grid(width, height)
  common.rect(grid, 2 * verts + 2, height, 0, 0, 5)
  common.rect(grid, 2 * verts + 1, 2 * horizs + 1, 0, 0, 0)
  for cdir, ival, oval, color in zip(cdirs, ivals, ovals, colors):
    if cdir == 1:
      for r in range(2 * horizs + 1):
        grid[r][ival] = color
      for r in range(height):
        if r == 0 or r + 1 == height or output[r][oval] != 0:
          grid[r][2 * verts + 2 + oval] = 4
        output[r][oval] = color
    else:
      for c in range(2 * verts + 1):
        grid[ival][c] = color
      for c in range(width):
        if c == 0 or c + 1 == width or output[oval][c] != 0:
          grid[oval][2 * verts + 2 + c] = 4
        output[oval][c] = color
  if erows:
    for erow, ecol, egrid, ecolor in zip(erows, ecols, egrids, ecolors):
      if egrid == 1: grid[erow][ecol] = ecolor
      else: output[erow][ecol] = ecolor
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=11, cdirs=[0, 0, 1, 1], ivals=[1, 3, 1, 3],
               ovals=[3, 7, 2, 5], colors=[2, 3, 1, 1], flop=False),
      generate(height=9, cdirs=[1, 1, 0, 0], ivals=[1, 3, 1, 3],
               ovals=[1, 5, 1, 6], colors=[2, 1, 3, 3], flop=False),
      generate(height=7, cdirs=[0, 1, 1], ivals=[1, 3, 1], ovals=[4, 4, 2],
               colors=[1, 2, 3], flop=True),
      generate(height=9, cdirs=[0, 1, 0], ivals=[3, 1, 1], ovals=[5, 4, 2],
               colors=[2, 1, 3], flop=False),
  ]
  test = [
      generate(height=12, cdirs=[0, 1, 1, 1, 0], ivals=[1, 1, 3, 5, 3],
               ovals=[4, 1, 3, 5, 9], colors=[3, 2, 2, 2, 1], flop=True,
               erows=[1, 3, 4, 9], ecols=[3, 3, 3, 3, 3], egrids=[1, 1, 0, 0],
               ecolors=[3, 2, 3, 2]),
  ]
  return {"train": train, "test": test}
