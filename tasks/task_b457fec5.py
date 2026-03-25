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


def generate(width=None, height=None, legend=None, thick=None, colors=None,
             lengths=None, brows=None, bcols=None, cdirs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    legend: The column of the legend.
    thick: The thickness of the squares.
    colors: The colors of the legend.
    lengths: The lengths of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    cdirs: The directions of the boxes.
  """

  def draw():
    if common.overlaps(brows, bcols, lengths, lengths): return None, None
    grid, output = common.grids(width, height)
    ids = common.grid(width, height, -1)
    for j, (length, brow, bcol, cdir) in enumerate(zip(lengths, brows, bcols, cdirs)):
      for i in range(length - thick + 1):
        row = brow + i
        col = (bcol + i) if cdir == 1 else (bcol + length - thick - i)
        color = colors[i % len(colors)]
        common.rect(grid, thick, thick, row, col, 5)
        common.rect(output, thick, thick, row, col, color)
        common.rect(ids, thick, thick, row, col, j)
    # Check that no two boxes are directly adjacent.
    for r in range(1, height - 1):
      for c in range(1, width - 1):
        if ids[r][c] == -1: continue
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if ids[r + dr][c + dc] not in [-1, ids[r][c]]: return None, None
    # Check that the legend won't touch anything.
    for r in range(0, 3):
      for c in range(legend - 1, legend + len(colors) + 1):
        if grid[r][c] != 0: return None, None
    # Now draw the legend.
    for i, color in enumerate(colors):
      output[1][legend + i] = grid[1][legend + i] = color
    return grid, output

  if width is None:
    colors = common.sample([1, 2, 3, 4, 8], common.randint(3, 4))
    thick = len(colors) + common.randint(0, 1)
    num_boxes = common.randint(1, 3)
    while True:
      width, height = common.randint(18, 27), common.randint(18, 27)
      legend = common.randint(1, width - len(colors) - 1)
      min_len, max_len = thick + len(colors) - 1, min(width, height)
      lengths = [common.randint(min_len, max_len) for _ in range(num_boxes)]
      brows = [common.randint(0, height - length) for length in lengths]
      bcols = [common.randint(0, width - length) for length in lengths]
      cdirs = [2 * common.randint(0, 1) - 1 for _ in range(num_boxes)]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=17, legend=9, thick=3, colors=[1, 3, 4], lengths=[11], brows=[3], bcols=[2], cdirs=[-1]),
      generate(width=19, height=23, legend=1, thick=4, colors=[1, 2, 3, 8], lengths=[15], brows=[4], bcols=[1], cdirs=[1]),
      generate(width=18, height=14, legend=2, thick=4, colors=[2, 8, 3], lengths=[6, 9], brows=[1, 3], bcols=[11, 1], cdirs=[-1, 1]),
  ]
  test = [
      generate(width=23, height=27, legend=6, thick=5, colors=[1, 3, 4, 2], lengths=[8, 12, 12], brows=[1, 3, 15], bcols=[14, 1, 1], cdirs=[-1, 1, 1]),
  ]
  return {"train": train, "test": test}
