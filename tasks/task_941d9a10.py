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


def generate(wides=None, talls=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: a list of spacing widths
    talls: a list of spacing heights
  """
  if wides is None:
    while True:
      wides = [common.randint(1, 4) for _ in range(2 * common.randint(1, 2) + 1)]
      talls = [common.randint(1, 3) for _ in range(2 * common.randint(1, 2) + 1)]
      if sum(wides) + len(wides) - 1 != 10: continue
      if sum(talls) + len(talls) - 1 != 10: continue
      break

  width, height = sum(wides) + len(wides) - 1, sum(talls) + len(talls) - 1
  grid, output = common.grids(width, height)
  r = -1
  for tall in talls:
    r += tall + 1
    if r >= height: break
    for c in range(width):
      output[r][c] = grid[r][c] = common.gray()
  c = -1
  for wide in wides:
    c += wide + 1
    if c >= width: break
    for r in range(height):
      output[r][c] = grid[r][c] = common.gray()
  for r in range(talls[0]):
    for c in range(wides[0]):
      output[r][c] = common.blue()
  roff = sum(talls[0:len(talls) // 2]) + len(talls) // 2
  coff = sum(wides[0:len(wides) // 2]) + len(wides) // 2
  for r in range(talls[len(talls) // 2]):
    for c in range(wides[len(wides) // 2]):
      output[roff + r][coff + c] = common.red()
  roff = sum(talls[0:len(talls) - 1]) + len(talls) - 1
  coff = sum(wides[0:len(wides) - 1]) + len(wides) - 1
  for r in range(talls[-1]):
    for c in range(wides[-1]):
      output[roff + r][coff + c] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[2, 4, 2], talls=[3, 3, 2]),
      generate(wides=[3, 4, 1], talls=[1, 1, 2, 1, 1]),
      generate(wides=[1, 2, 1, 1, 1], talls=[3, 2, 3]),
  ]
  test = [
      generate(wides=[1, 1, 2, 1, 1], talls=[1, 2, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
