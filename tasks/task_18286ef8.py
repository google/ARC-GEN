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


def generate(wides=None, talls=None, prows=None, pcols=None, pids=None,
             pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the outer columns.
    talls: The heights of the outer rows.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    pids: The pids of the pixels (0 = northwest, 1 = north, etc.)
    pcolors: The colors of the pixels.
  """

  if wides is None:
    wides = common.choices(list(range(1, 10)), 2)
    talls = common.choices(list(range(1, 10)), 2)
    prows, pcols, pids = [], [], []
    seen = set()
    for _ in range(common.randint(4, 10)):
      wide, tall = 3, 3
      pid = common.choice([0, 1, 2, 3, 5, 6, 7, 8])
      if pid in [0, 3, 6]: wide = wides[0]
      if pid in [2, 5, 8]: wide = wides[1]
      if pid in [0, 1, 2]: tall = talls[0]
      if pid in [6, 7, 8]: tall = talls[1]
      prow = common.randint(0, tall - 1)
      pcol = common.randint(0, wide - 1)
      if (pid, prow, pcol) in seen: continue
      seen.add((pid, prow, pcol))
      prows.append(prow)
      pcols.append(pcol)
      pids.append(pid)
    pcolors = common.choices([1, 2, 3, 4, 8], len(prows))
    pcolors[common.randint(0, len(pcolors) - 1)] = 6

  width, height = sum(wides) + 5, sum(talls) + 5
  grid, output = common.grids(width, height, 7)
  # Draw the grid.
  for r in range(height):
    output[r][wides[0]] = grid[r][wides[0]] = 0
    output[r][wides[0] + 4] = grid[r][wides[0] + 4] = 0
  for c in range(width):
    output[talls[0]][c] = grid[talls[0]][c] = 0
    output[talls[0] + 4][c] = grid[talls[0] + 4][c] = 0
  common.rect(grid, 3, 3, talls[0] + 1, wides[0] + 1, 5)
  common.rect(output, 3, 3, talls[0] + 1, wides[0] + 1, 5)
  mrow, mcol = 0, 0
  for prow, pcol, pid, pcolor in zip(prows, pcols, pids, pcolors):
    if pid in [1, 4, 7]: pcol += wides[0] + 1
    if pid in [2, 5, 8]: pcol += wides[0] + 5
    if pid in [3, 4, 5]: prow += talls[0] + 1
    if pid in [6, 7, 8]: prow += talls[0] + 5
    grid[prow][pcol] = pcolor
    output[prow][pcol] = 9 if pcolor == 6 else pcolor
    if pcolor != 6: continue
    if pid in [0, 3, 6]: mcol = -1
    if pid in [2, 5, 8]: mcol = 1
    if pid in [0, 1, 2]: mrow = -1
    if pid in [6, 7, 8]: mrow = 1
  grid[talls[0] + 2][wides[0] + 2] = 9
  output[talls[0] + 2 + mrow][wides[0] + 2 + mcol] = 9
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[3, 4], talls=[3, 4], prows=[2, 1, 0, 1, 2, 2],
               pcols=[2, 2, 0, 3, 2, 2], pids=[0, 2, 3, 5, 6, 8],
               pcolors=[2, 4, 4, 8, 8, 6]),
      generate(wides=[2, 1], talls=[2, 1], prows=[0, 0, 0, 0],
               pcols=[0, 2, 0, 1], pids=[0, 1, 3, 6], pcolors=[1, 4, 6, 3]),
      generate(wides=[6, 4], talls=[3, 7], prows=[0, 2, 1, 1, 1, 1, 4, 4, 2, 4],
               pcols=[5, 1, 1, 2, 0, 1, 4, 1, 3, 3],
               pids=[0, 0, 1, 2, 5, 6, 6, 7, 8, 8],
               pcolors=[8, 6, 1, 2, 8, 4, 2, 1, 1, 1]),
  ]
  test = [
      generate(wides=[5, 9], talls=[7, 7], prows=[4, 1, 0, 2, 0, 2, 5, 2, 4, 6],
               pcols=[0, 3, 6, 3, 2, 0, 2, 2, 4, 8],
               pids=[1, 3, 5, 6, 7, 7, 7, 8, 8, 8],
               pcolors=[8, 4, 3, 4, 3, 6, 8, 2, 2, 8]),
  ]
  return {"train": train, "test": test}
