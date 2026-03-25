# Copyright 2025 Google LLC
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


def generate(wide=None, tall=None, patches=None, lengths=None, depths=None,
             rowoffset=None, coloffset=None, size=21):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: the width of the patch grid
    tall: the height of the patch grid
    patches: the colors in the patch grid
    lengths: the lengths of the patches
    depths: the depths of the patches
    rowoffset: the row offset for the quilt
    coloffset: the column offset for the quilt
    size: the width and height of the input grid
  """
  if wide is None:
    # TODO: Make sure two adjacent rows (or columns) are not the same.
    wide, tall = common.randint(2, 3), common.randint(2, 3)
    while True:  # Make sure there isn't an "L" of the same color.
      patches, el = [common.random_color() for _ in range(wide * tall)], False
      for r in range(tall):
        for c in range(wide):
          color, same = patches[r * wide + c], 0
          if r > 0 and color == patches[(r - 1) * wide + c]: same += 1
          if r < tall - 1 and color == patches[(r + 1) * wide + c]: same += 1
          if c > 0 and color == patches[r * wide + c - 1]: same += 1
          if c < wide - 1 and color == patches[r * wide + c + 1]: same += 1
          if same > 1: el = True
      if el: continue
      legal = True
      # Check rows to see if any two are identical.
      for r in range(tall):
        for rp in range(r):
          same = True
          for c in range(wide):
            if patches[r * wide + c] != patches[rp * wide + c]: same = False
          if same: legal = False
      # Check cols to see if any two are identical.
      for c in range(wide):
        for cp in range(c):
          same = True
          for r in range(tall):
            if patches[r * wide + c] != patches[r * wide + cp]: same = False
          if same: legal = False
      if legal: break
    while True:
      lengths = [common.randint(3, 12) for _ in range(wide)]
      depths = [common.randint(3, 12) for _ in range(tall)]
      if sum(lengths) < size and sum(depths) < size: break
    rowoffset = common.randint(0, size - sum(depths))
    coloffset = common.randint(0, size - sum(lengths))

  grid, output = common.grid(size, size), common.grid(wide, tall)
  for row in range(tall):
    for col in range(wide):
      output[row][col] = patches[row * wide + col]
      for dr in range(depths[row]):
        for dc in range(lengths[col]):
          r = rowoffset + sum(depths[:row]) + dr
          c = coloffset + sum(lengths[:col]) + dc
          grid[r][c] = output[row][col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=3, tall=3, patches=[8, 7, 7, 3, 4, 1, 2, 5, 5],
               lengths=[8, 6, 6], depths=[6, 4, 5], rowoffset=1, coloffset=1),
      generate(wide=2, tall=2, patches=[2, 8, 1, 4], lengths=[7, 8],
               depths=[8, 7], rowoffset=1, coloffset=1),
      generate(wide=2, tall=3, patches=[8, 2, 3, 3, 4, 1], lengths=[6, 6],
               depths=[5, 6, 6], rowoffset=2, coloffset=2),
  ]
  test = [
      generate(wide=3, tall=3, patches=[2, 4, 1, 8, 3, 8, 2, 4, 2],
               lengths=[5, 8, 5], depths=[6, 8, 4], rowoffset=1, coloffset=1),
  ]
  return {"train": train, "test": test}
