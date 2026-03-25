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


def generate(tops=None, lefts=None, rights=None, bottoms=None):
  """Returns input and output grids according to the given parameters.

  Args:
    tops: The lengths of the top lines.
    lefts: The lengths of the left lines.
    rights: The lengths of the right lines.
    bottoms: The lengths of the bottom lines.
  """

  def draw(multi_diags=True):
    grid, output = common.grids(10, 10)
    def put(i, j):
      output[i][j] = grid[i][j] = 5
    for i in range(10):
      for j in range(tops[i]): put(j, i)
      for j in range(lefts[i]): put(i, j)
      for j in range(rights[i]): put(i, 9 - j)
      for j in range(bottoms[i]): put(9 - j, i)
    if not common.all_connected(grid, 0): return None, None
    longest, diags = -1, []
    for diag_dir in [1, -1]:
      for diag in range(-10, 10):
        length = 0
        for r in range(10):
          c = (r - diag) if diag_dir == 1 else (9 - r - diag)
          if c < 0 or c >= 10: continue
          if grid[r][c] == 0: length += 1
        if length < longest: continue
        if length > longest: diags.clear()
        diags.append((diag_dir, diag))
        longest = length
    if not multi_diags and len(diags) > 1: return None, None
    while True:
      if len(diags) > 1: diags.pop()
      if len(diags) <= 1: break
      if len(diags) > 1: diags.pop(0)
      if len(diags) <= 1: break
    for diag in diags:
      diag_dir, diag_val = diag
      for r in range(10):
        for c in range(10):
          if diag_dir == 1:
            if output[r][c] == 0 and r - c == diag_val: output[r][c] = 8
          if diag_dir == -1:
            if output[r][c] == 0 and 9 - r - c == diag_val: output[r][c] = 8
    return grid, output

  if tops is None:
    lengths = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    while True:
      tops = [common.choice(lengths) for _ in range(10)]
      lefts = [common.choice(lengths) for _ in range(10)]
      rights = [common.choice(lengths) for _ in range(10)]
      bottoms = [common.choice(lengths) for _ in range(10)]
      grid, _ = draw(multi_diags=False)
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(tops=[1, 1, 1, 1, 1, 1, 3, 2, 2, 1],
               lefts=[1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
               rights=[1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
               bottoms=[1, 2, 2, 3, 3, 1, 2, 2, 1, 1]),
      generate(tops=[1, 3, 2, 1, 3, 1, 2, 1, 1, 1],
               lefts=[1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
               rights=[1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
               bottoms=[1, 2, 1, 2, 1, 1, 2, 3, 3, 1]),
      generate(tops=[1, 4, 3, 1, 1, 1, 2, 3, 3, 1],
               lefts=[1, 3, 3, 2, 1, 1, 3, 2, 3, 1],
               rights=[1, 4, 3, 1, 2, 1, 1, 2, 2, 1],
               bottoms=[1, 4, 2, 1, 4, 4, 2, 1, 3, 1]),
      generate(tops=[1, 1, 1, 1, 2, 3, 1, 1, 2, 1],
               lefts=[1, 1, 2, 3, 2, 1, 2, 1, 1, 1],
               rights=[1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
               bottoms=[1, 2, 1, 3, 2, 4, 1, 2, 1, 1]),
  ]
  test = [
      generate(tops=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               lefts=[1, 3, 2, 3, 1, 1, 1, 1, 1, 1],
               rights=[1, 2, 2, 1, 3, 4, 1, 1, 1, 1],
               bottoms=[1, 2, 2, 3, 3, 2, 2, 3, 1, 1]),
  ]
  return {"train": train, "test": test}
