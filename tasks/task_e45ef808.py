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


def generate(lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: A list of lengths to use.
  """

  if lengths is None:
    while True:
      length, lengths = common.randint(1, 7), []
      for _ in range(12):
        lengths.append(length)
        # Adjust the column.
        length += common.randint(-1, 1)
        # Sometimes, adjust it even more.
        if common.randint(0, 9): length += common.randint(-1, 1)
        if length < 1: length = 1
        if length > 7: length = 7
      if len(set(lengths)) >= 5: break

  grid, output = common.grids(12, 12, 1)
  for c in range(12):
    output[0][c] = grid[0][c] = 0
  for c, length in enumerate(lengths):
    for r in range(length):
      output[11 - r][c] = grid[11 - r][c] = 6
  # Find rightmost tallest.
  pos = 0
  for c in range(12):
    if lengths[c] >= lengths[pos]: pos = c
  for r in range(1, 12 - lengths[pos]):
    output[r][pos] = 4
  # Find leftmost shortest.
  pos = 11
  for c in range(11, -1, -1):
    if lengths[c] <= lengths[pos]: pos = c
  for r in range(1, 12 - lengths[pos]):
    output[r][pos] = 9
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[5, 4, 3, 3, 2, 3, 4, 5, 7, 6, 5, 4]),
      generate(lengths=[1, 2, 3, 2, 2, 3, 4, 5, 4, 3, 4, 5]),
  ]
  test = [
      generate(lengths=[3, 4, 4, 3, 4, 5, 6, 5, 4, 4, 3, 2]),
  ]
  return {"train": train, "test": test}
