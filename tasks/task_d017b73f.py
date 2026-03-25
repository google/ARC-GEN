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


def generate(hlengths=None, hrows=None, vlengths=None, vcolors=[], voffsets=None, bump=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  def draw():
    inwidth, inheight = sum(vlengths) + len(vlengths) - 1 + bump, 3
    outwidth, outheight = sum(hlengths) - len(hlengths) + 1, 3
    grid = common.grid(inwidth, inheight)
    output = common.grid(outwidth, outheight)
    def put_in(row, col, color):
      if row < 0 or col < 0 or row >= inheight or col >= inwidth:
        return False
      grid[row][col] = color
      return True
    def put_out(row, col, color):
      if row < 0 or col < 0 or row >= outheight or col >= outwidth:
        return False
      output[row][col] = color
      return True
    in_column = 0
    out_colors, out_offsets, in_columns = [], [], []
    for vlength, vcolor, voffset in zip(vlengths, vcolors, voffsets):
      for _ in range(vlength):
        out_colors.append(vcolor)
        out_offsets.append(voffset)
        in_columns.append(in_column)
        in_column += 1
      in_column += 1
    outcol, last_row = 0, None
    for hlength, hrow in zip(hlengths, hrows):
      if last_row is not None:
        for row in range(min(hrow, last_row), max(hrow, last_row) + 1):
          if not put_in(row + out_offsets[outcol], in_columns[outcol], out_colors[outcol]):
            return None, None
          if not put_out(row, outcol, out_colors[outcol]):
            return None, None
      for _ in range(hlength):
        if not put_in(hrow + out_offsets[outcol], in_columns[outcol], out_colors[outcol]):
          return None, None
        if not put_out(hrow, outcol, out_colors[outcol]):
          return None, None
        outcol += 1
      outcol -= 1
      last_row = hrow
    return grid, output

  if hlengths is None:
    bump = common.randint(0, 1)
    while True:
      hlengths = [common.randint(2, 3)]
      for _ in range(common.randint(3, 4)):
        hlengths.append(common.randint(3, 5))
      if common.randint(0, 1):
        hlengths.append(1)
      hrows = []
      for _ in hlengths:
        if not hrows:
          hrows.append(1)  # Always start in the center.
        else:
          choices = list(range(3))
          choices.remove(hrows[-1])
          hrows.append(common.choice(choices))
      outwidth = sum(hlengths) - len(hlengths) + 1
      vlengths = [common.randint(2, 3) for _ in range(common.randint(3, 4))]
      if sum(vlengths) != outwidth: continue
      vcolors = [common.random_color() for _ in vlengths]
      voffsets = [common.randint(-2, 2) for _ in vlengths]
      voffsets[0] = 0  # Always start in the center.
      if len(set(voffsets)) == 1: continue  # Need to shift at least something.
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(hlengths=[3, 4, 4], hrows=[1, 2, 1], vlengths=[3, 3, 3], vcolors=[2, 8, 6], voffsets=[0, -1, 1], bump=0),
      generate(hlengths=[2, 5, 3, 1], hrows=[1, 2, 1, 2], vlengths=[2, 2, 2, 2], vcolors=[2, 3, 1, 2], voffsets=[0, -2, -1, -1], bump=0),
      generate(hlengths=[2, 4, 3, 2], hrows=[1, 0, 1, 0], vlengths=[3, 2, 3], vcolors=[1, 2, 2], voffsets=[0, 1, 0], bump=1),
      generate(hlengths=[2, 3, 4], hrows=[1, 0, 1], vlengths=[2, 2, 3], vcolors=[2, 1, 2], voffsets=[0, 1, 0], bump=0),
  ]
  test = [
      generate(hlengths=[2, 3, 3, 3, 1], hrows=[1, 0, 2, 1, 2], vlengths=[2, 2, 2, 2], vcolors=[2, 1, 3, 5], voffsets=[0, 0, -1, -1], bump=0),
  ]
  return {"train": train, "test": test}
