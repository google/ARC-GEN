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


def generate(vcols=None, vlengths=None, vcolors=None, hrows=None, hlengths=None,
             hcolors=None, hsides=None):
  """Returns input and output grids according to the given parameters.

  Args:
    vcols: Vertical column indices.
    vlengths: Vertical lengths.
    vcolors: Vertical colors.
    hrows: Horizontal row indices.
    hlengths: Horizontal lengths.
    hcolors: Horizontal colors.
    hsides: Horizontal sides.
  """

  def draw():
    if 0 not in hsides or 1 not in hsides: return None, None
    rows = [hrow for hrow, hside in zip(hrows, hsides) if hside in [0, 2]]
    if common.overlaps_1d(rows, [2] * len(rows)): return None, None
    rows = [hrow for hrow, hside in zip(hrows, hsides) if hside in [1, 2]]
    if common.overlaps_1d(rows, [2] * len(rows)): return None, None
    grid, output = common.grids(15, 15)
    for hrow, hlength, hcolor, hside in zip(hrows, hlengths, hcolors, hsides):
      for col in range(hlength):
        if grid[hrow][col if hside == 0 else (14 - col)]: return None, None
        grid[hrow][col if hside == 0 else (14 - col)] = hcolor
        output[hrow][col if hside == 0 else (14 - col)] = hcolor
    for vcol, vlength, vcolor in zip(vcols, vlengths, vcolors):
      color = vcolor
      for row in range(15):
        if output[14 - row][vcol - 1] != output[14 - row][vcol + 1]:
          return None, None  # Just one color on one side is ill-defined.
        if output[14 - row][vcol - 1]: color = output[14 - row][vcol - 1]
        grid[14 - row][vcol] = vcolor if row < vlength else 0
        output[14 - row][vcol] = vcolor if row < vlength else color
    return grid, output

  if vcols is None:
    mid = common.randint(6, 8)
    vcols = [common.randint(1, mid - 2), common.randint(mid + 2, 13)]
    vcolors = common.random_colors(2)
    vlengths = [common.randint(1, 6), common.randint(1, 6)]
    while True:
      num_hrows = common.randint(2, 6)
      hrows = [common.randint(1, 14 - max(vlengths)) for _ in range(num_hrows)]
      hsides = [common.randint(0, 1) for _ in range(num_hrows)]
      if common.randint(0, 1): hsides[0] = 2
      hcolors = common.random_colors(num_hrows, exclude=list(set(vcolors)))
      hlengths = []
      for hside in hsides:
        if hside == 0:
          hlengths.append(mid + common.randint(0, 1))
        elif hside == 1:
          hlengths.append(15 - mid + common.randint(0, 1))
        else:
          hlengths.append(15)
      grid, _ = draw()
      if grid: break
    print(mid, hsides, hlengths)

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(vcols=[3, 9], vlengths=[4, 6], vcolors=[1, 5],
               hrows=[3, 6, 8, 8], hlengths=[7, 9, 7, 8], hcolors=[3, 6, 4, 7],
               hsides=[0, 1, 0, 1]),
      generate(vcols=[3, 9], vlengths=[4, 3], vcolors=[3, 4], hrows=[9, 9],
               hlengths=[8, 7], hcolors=[2, 3], hsides=[0, 1]),
      generate(vcols=[1, 9], vlengths=[1, 1], vcolors=[1, 1],
               hrows=[2, 3, 5, 8, 11, 11], hlengths=[9, 6, 10, 6, 6, 9],
               hcolors=[7, 8, 6, 3, 9, 5], hsides=[1, 0, 1, 0, 0, 1]),
  ]
  test = [
      generate(vcols=[3, 8], vlengths=[2, 1], vcolors=[6, 8],
               hrows=[2, 3, 6, 8, 11], hlengths=[6, 9, 7, 9, 15],
               hcolors=[2, 5, 3, 9, 4], hsides=[0, 1, 0, 1, 2]),
  ]
  return {"train": train, "test": test}
