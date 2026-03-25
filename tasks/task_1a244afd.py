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


def generate(size=None, brows=None, bcols=None, prows=None, pcols=None, icolor=6, ocolor=7, bgcolor=8):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    brows: The rows of the blue pixels.
    bcols: The columns of the blue pixels.
    prows: The rows of the pink pixels.
    pcols: The columns of the pink pixels.
  """

  def draw():
    # First, match the blue pixels to the pink pixels.
    b_to_p, p_to_b = [-1] * len(brows), [-1] * len(brows)
    for _ in range(len(brows) + 1):  # An upper bound on the number of rounds.
      for i in range(len(prows)):
        if p_to_b[i] != -1: continue  # Already matched.
        candidates = []
        for j in range(len(brows)):
          if b_to_p[j] != -1: continue  # Already matched.
          if prows[i] == brows[j] or pcols[i] == bcols[j]: candidates.append(j)
        if len(candidates) != 1: continue
        p_to_b[i], b_to_p[candidates[0]] = candidates[0], i
    if -1 in b_to_p or -1 in p_to_b: return None, None  # Failed to match.
    # Second, draw all pixels.
    grid, output = common.grids(size, size, bgcolor)
    for b, (brow, bcol) in enumerate(zip(brows, bcols)):
      if grid[brow][bcol] != bgcolor: return None, None
      if output[brow][bcol] != bgcolor: return None, None
      output[brow][bcol] = grid[brow][bcol] = 1
      p = b_to_p[b]
      if prows[p] < 0 or prows[p] >= size or pcols[p] < 0 or pcols[p] >= size:
        return None, None  # This pixel must be visible.
      if grid[prows[p]][pcols[p]] != bgcolor: return None, None
      grid[prows[p]][pcols[p]] = icolor
      dist = max(abs(brows[b] - prows[p]), abs(bcols[b] - pcols[p]))
      orow, ocol = brows[b], bcols[b]
      if brows[b] < prows[p]: ocol = bcols[b] + dist
      if brows[b] > prows[p]: ocol = bcols[b] - dist
      if bcols[b] < pcols[p]: orow = brows[b] - dist
      if bcols[b] > pcols[p]: orow = brows[b] + dist
      if common.get_pixel(output, orow, ocol) not in [-1, bgcolor]:
        return None, None
      common.draw(output, orow, ocol, ocolor)
    return grid, output

  if size is None:
    size = common.randint(8, 16)
    num_pixels = common.randint(size // 4, size // 2)
    while True:
      brows = [common.randint(0, size - 1) for _ in range(num_pixels)]
      bcols = [common.randint(0, size - 1) for _ in range(num_pixels)]
      dists = [common.randint(1, 4) for _ in range(num_pixels)]
      angles = [common.randint(0, 3) for _ in range(num_pixels)]
      prows, pcols = [], []
      for brow, bcol, dist, angle in zip(brows, bcols, dists, angles):
        prow, pcol = brow, bcol
        if angle == 0: prow -= dist
        if angle == 1: prow += dist
        if angle == 2: pcol -= dist
        if angle == 3: pcol += dist
        prows, pcols = prows + [prow], pcols + [pcol]
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=16, brows=[3, 4, 9, 11], bcols=[11, 5, 10, 4],
               prows=[0, 3, 8, 15], pcols=[5, 14, 10, 4]),
      generate(size=10, brows=[2, 5, 6], bcols=[4, 6, 2],
               prows=[1, 6, 6], pcols=[4, 0, 6]),
      generate(size=8, brows=[0, 4, 5], bcols=[0, 5, 2], prows=[0, 2, 6],
               pcols=[1, 5, 2]),
  ]
  test = [
      generate(size=16, brows=[3, 3, 4, 9, 14, 14, 14],
               bcols=[0, 13, 6, 11, 2, 7, 13],
               prows=[2, 4, 4, 8, 11, 13, 14], pcols=[0, 8, 13, 11, 7, 2, 10]),
  ]
  return {"train": train, "test": test}
