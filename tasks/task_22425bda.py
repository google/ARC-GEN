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


def generate(size=None, colors=None, cdirs=None, vals=None,
             allow_ambiguous=False):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the lines.
    cdirs: The directions of the lines.
    vals: The values of the lines.
    allow_ambiguous: Whether to allow ambiguous cases.
  """

  def draw():
    grid, output = common.grid(size, size, 7), [[]]
    last_color = -1
    special_cells = []
    for color, cdir, val in zip(colors, cdirs, vals):
      covered = False
      output[0].append(color)
      for row in range(size):
        for col in range(size):
          if cdir == 0 and row != val: continue
          if cdir == 1 and col != val: continue
          if cdir == 2 and row - col != val: continue
          if cdir == 3 and row + col - size + 1 != val: continue
          if (row, col) in special_cells and not allow_ambiguous:
            return None, None
          if grid[row][col] == last_color:
            if covered: return None, None  # Should only cover at one pixel.
            covered = True
            special_cells.append((row, col))
          grid[row][col] = color
      if last_color != -1 and not covered: return None, None
      last_color = color
    return grid, output

  if size is None:
    size = common.randint(6, 18)
    segments = size // 3
    colors = common.random_colors(segments, exclude=[7])
    while True:
      cdirs = [common.randint(0, 3) for _ in range(segments)]
      vals = []
      for cdir in cdirs:
        lower, upper = 1, size - 2
        if cdir in [2, 3]: lower, upper = -(size // 2), size // 2
        vals.append(common.randint(lower, upper))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, colors=[2, 5], cdirs=[1, 0], vals=[3, 3]),
      generate(size=10, colors=[0, 8, 9], cdirs=[0, 1, 2], vals=[4, 6, 0]),
      generate(size=12, colors=[3, 2, 1, 5], cdirs=[1, 0, 2, 1],
               vals=[4, 5, -1, 8]),
      generate(size=16, colors=[4, 1, 9, 3, 5], cdirs=[1, 0, 1, 0, 1],
               vals=[14, 14, 12, 12, 10]),
  ]
  test = [
      # This next one is arguably ambiguous (the ordering of 9 and 1 is unclear)
      generate(size=16, colors=[5, 4, 0, 9, 1, 3], cdirs=[3, 1, 2, 0, 2, 3],
               vals=[-6, 6, 5, 7, -7, 6], allow_ambiguous=True),
  ]
  return {"train": train, "test": test}
