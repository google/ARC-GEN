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


def generate(wides=None, talls=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    colors: A list of colors to use.
  """

  if wides is None:
    num_wides, num_talls = common.randint(2, 5), common.randint(2, 5)
    while True:
      wides = [common.randint(2, 10) for _ in range(num_wides)]
      talls = [common.randint(2, 10) for _ in range(num_talls)]
      colors = [common.random_color() for _ in range(num_wides * num_talls)]
      if sum(wides) < 12 or sum(wides) > 15: continue
      if sum(talls) < 12 or sum(talls) > 15: continue
      good = True
      for r in range(1, num_talls):
        some_diff = False
        for c in range(num_wides):
          if colors[r * num_wides + c] != colors[(r - 1) * num_wides + c]:
            some_diff = True
        if not some_diff: good = False
      for c in range(1, num_wides):
        some_diff = False
        for r in range(num_talls):
          if colors[r * num_wides + c] != colors[r * num_wides + c - 1]:
            some_diff = True
        if not some_diff: good = False
      if good: break

  grid = common.grid(sum(wides), sum(talls))
  output = common.grid(len(wides), len(talls))
  for i, color in enumerate(colors):
    row, col = i // len(wides), i % len(wides)
    output[row][col] = color
    for r in range(talls[row]):
      for c in range(wides[col]):
        grid[sum(talls[:row]) + r][sum(wides[:col]) + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[3, 5, 6], talls=[5, 10], colors=[1, 2, 8, 5, 6, 3]),
      generate(wides=[5, 3, 6], talls=[4, 8], colors=[4, 5, 2, 1, 3, 2]),
      generate(wides=[3, 5, 4, 3], talls=[4, 5, 6],
               colors=[8, 7, 9, 8, 3, 1, 6, 4, 2, 4, 1, 5]),
      generate(wides=[4, 11], talls=[9, 4], colors=[2, 8, 3, 5]),
  ]
  test = [
      generate(wides=[4, 4, 5, 2], talls=[2, 3, 5, 2, 3],
               colors=[8, 7, 4, 8, 3, 1, 2, 8, 4, 5, 3, 9, 2, 6, 1, 7, 1, 5, 2, 8]),
  ]
  return {"train": train, "test": test}
