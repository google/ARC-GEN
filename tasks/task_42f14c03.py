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


def generate(hwides=None, htalls=None, hrows=None, hcols=None, htops=None, hbottoms=None, hcolors=None,
             iwides=None, italls=None, irows=None, icols=None, itops=None, ibottoms=None, icolors=None,
             toprow=None, topcol=None, topcolor=None, bottomrow=None, bottomcol=None, bottomcolor=None, bgcolor=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if hwides is None:
    num_i, num_h, xpose = 1, common.randint(1, 2), common.randint(0, 1)
    while True:
      hwides, htalls, hrows, hcols, htops, hbottoms = [], [], [], [], [], []
      first_notch_area, good = None, True
      for _ in range(num_h):
        hwide, htall = common.randint(4, 5), common.randint(3, 7)
        hrow, hcol = common.randint(0, 16 - htall), common.randint(0, 16 - hwide)
        while True:
          htop, hbottom = common.randint(1, htall - 1), common.randint(1, htall - 1)
          if htop + hbottom < htall: break
        notch_area = (htop + hbottom) * (hwide - 2)
        if first_notch_area is None: first_notch_area = notch_area
        elif first_notch_area == notch_area: good = False
        hwides.append(hwide)
        htalls.append(htall)
        hrows.append(hrow)
        hcols.append(hcol)
        htops.append(htop)
        hbottoms.append(hbottom)
      toprow = common.randint(0, 16 - htops[0])
      topcol = common.randint(0, 16 - hwides[0] + 2)
      bottomrow = common.randint(0, 16 - hbottoms[0])
      bottomcol = common.randint(0, 16 - hwides[0] + 2)
      iwides, italls, irows, icols, itops, ibottoms = [], [], [], [], [], []
      for _ in range(num_i):
        iwide, itall = common.randint(4, 5), common.randint(3, 7)
        irow, icol = common.randint(0, 16 - itall), common.randint(0, 16 - iwide)
        while True:
          itop, ibottom = common.randint(0, iwide - 1), common.randint(1, iwide - 1)
          if itop + ibottom > 0 and itop + ibottom < iwide: break
        notch_area = (itop + ibottom) * (itall - 2)
        if first_notch_area is None: first_notch_area = notch_area
        elif first_notch_area == notch_area: good = False
        iwides.append(iwide)
        italls.append(itall)
        irows.append(irow)
        icols.append(icol)
        itops.append(itop)
        ibottoms.append(ibottom)
      if not good: continue  # Some ambiguuity about which shape the notches fit
      # Now to check for overlap
      rows = hrows + irows + [toprow, bottomrow]
      cols = hcols + icols + [topcol, bottomcol]
      wides = hwides + iwides + [hwides[0] - 2, hwides[0] - 2]
      talls = htalls + italls + [htops[0], hbottoms[0]]
      if not common.overlaps(rows, cols, wides, talls, 1): break
    colors = common.shuffle(list(range(1, 10)))
    def get_color():
      return colors.pop()
    hcolors = [get_color() for _ in range(num_h)]
    icolors = [get_color() for _ in range(num_i)]
    topcolor = get_color()
    bottomcolor = get_color() if htops[0] != hbottoms[0] else topcolor
    bgcolor = get_color()

  grid = common.grid(16, 16, bgcolor)
  output = common.grid(hwides[0], htalls[0], hcolors[0])
  # Create the H's in the input grid.
  for hwide, htall, hrow, hcol, htop, hbottom, hcolor in zip(hwides, htalls, hrows, hcols, htops, hbottoms, hcolors):
    for r in range(htall):
      grid[hrow + r][hcol] = grid[hrow + r][hcol + hwide - 1] = hcolor
    for r in range(htall - htop - hbottom):
      for c in range(hcol + 1, hcol + hwide - 1):
        grid[hrow + htop + r][c] = hcolor
  # Create the I's in the input grid.
  for iwide, itall, irow, icol, itop, ibottom, icolor in zip(iwides, italls, irows, icols, itops, ibottoms, icolors):
    for c in range(iwide):
      grid[irow][icol + c] = grid[irow + itall - 1][icol + c] = icolor
    for r in range(irow + 1, irow + itall - 1):
      for c in range(iwide - itop - ibottom):
        grid[r][icol + itop + c] = icolor
  # Create the top & bottom notches in the input & output grids.
  for r in range(htops[0]):
    for c in range(hwides[0] - 2):
      grid[toprow + r][topcol + c] = topcolor
      output[r][c + 1] = topcolor
  for r in range(hbottoms[0]):
    for c in range(hwides[0] - 2):
      grid[bottomrow + r][bottomcol + c] = bottomcolor
      output[htalls[0] - 1 - r][c + 1] = bottomcolor
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(hwides=[4], htalls=[4], hrows=[2], hcols=[4], htops=[1],
               hbottoms=[1], hcolors=[3], iwides=[3], italls=[5], irows=[8],
               icols=[5], itops=[0], ibottoms=[1], icolors=[1], toprow=6,
               topcol=11, topcolor=6, bottomrow=11, bottomcol=1, bottomcolor=6,
               bgcolor=8, xpose=False),
      generate(hwides=[5, 4], htalls=[3, 6], hrows=[1, 2], hcols=[1, 8],
               htops=[1, 1], hbottoms=[1, 1], hcolors=[1, 3], iwides=[9],
               italls=[4], irows=[10], icols=[3], itops=[1], ibottoms=[1],
               icolors=[4], toprow=6, topcol=2, topcolor=8, bottomrow=14,
               bottomcol=13, bottomcolor=8, bgcolor=2, xpose=False),
      generate(hwides=[5], htalls=[6], hrows=[4], hcols=[3], htops=[2],
               hbottoms=[1], hcolors=[1], iwides=[6], italls=[4], irows=[9],
               icols=[9], itops=[3], ibottoms=[1], icolors=[2], toprow=2,
               topcol=10, topcolor=3, bottomrow=14, bottomcol=1, bottomcolor=6,
               bgcolor=4, xpose=True),
  ]
  test = [
      generate(hwides=[4, 4], htalls=[7, 3], hrows=[1, 2], hcols=[10, 2],
               htops=[2, 1], hbottoms=[3, 1], hcolors=[4, 1], iwides=[6],
               italls=[3], irows=[7], icols=[3], itops=[2], ibottoms=[2],
               icolors=[2], toprow=12, topcol=2, topcolor=3, bottomrow=12,
               bottomcol=9, bottomcolor=9, bgcolor=8, xpose=False),
  ]
  return {"train": train, "test": test}
