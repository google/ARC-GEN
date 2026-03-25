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


def generate(size=None, brows=None, bcols=None, cdirs=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The rows of the segments.
    bcols: The columns of the segments.
    cdirs: The directions of the segments.
    colors: The colors of the segments.
  """

  def draw():
    nonlocal size, brows, bcols, cdirs, colors
    # First, some basic checks.
    if len(set(cdirs)) < 2: return None, None
    wides = [2 - cdir for cdir in cdirs]
    talls = [1 + cdir for cdir in cdirs]
    if common.overlaps(brows, bcols, wides, talls): return None, None
    if common.some_abutted(brows, bcols, wides, talls): return None, None
    verts = [bcol for bcol, cdir in zip(bcols, cdirs) if cdir]
    horzs = [brow for brow, cdir in zip(brows, cdirs) if not cdir]
    if len(set(verts)) != len(verts): return None, None
    if len(set(horzs)) != len(horzs): return None, None
    # Second, draw the grids.
    grid, output = common.grids(size, size, 7)
    for the_dir in [1, 0]:
      for brow, bcol, cdir, color in zip(brows, bcols, cdirs, colors):
        if cdir != the_dir: continue
        grid[brow][bcol] = color
        grid[(brow + 1) if cdir else brow][bcol if cdir else (bcol + 1)] = color
        for i in range(size):
          output[i if cdir else brow][bcol if cdir else i] = color
    return grid, output

  if size is None:
    size = common.randint(6, 10)
    num_lines = size // 2 + common.randint(-1, 2)
    colors = common.choices([0, 1, 2, 3, 4, 5, 6, 8, 9], num_lines)
    while True:
      cdirs = [common.randint(0, 1) for _ in range(num_lines)]
      wides = [2 - cdir for cdir in cdirs]
      talls = [1 + cdir for cdir in cdirs]
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=8, brows=[1, 1, 2, 6], bcols=[1, 5, 3, 5],
               cdirs=[1, 0, 0, 0], colors=[9, 5, 5, 4]),
      generate(size=7, brows=[1, 2, 4, 5], bcols=[2, 4, 1, 4],
               cdirs=[1, 1, 0, 0], colors=[6, 2, 5, 1]),
      generate(size=9, brows=[1, 2, 2, 5, 7], bcols=[0, 4, 6, 6, 1],
               cdirs=[1, 1, 0, 0, 0], colors=[0, 1, 3, 0, 6]),
  ]
  test = [
      generate(size=10, brows=[1, 1, 2, 4, 5, 7, 7],
               bcols=[6, 8, 1, 3, 1, 4, 6], cdirs=[1, 1, 0, 0, 1, 1, 0],
               colors=[3, 1, 8, 8, 5, 2, 8]),
  ]
  return {"train": train, "test": test}
