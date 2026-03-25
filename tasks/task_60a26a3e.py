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


def generate(width=None, height=None, prows=None, pcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prows: The rows of the plusses.
    pcols: The columns of the plusses.
  """

  def draw():
    grid, output = common.grids(width, height)
    num_matches = 0
    # Draw the blue connecting lines.
    for i in range(len(prows)):
      for j in range(len(pcols)):
        if i == j: continue
        if prows[i] == prows[j] and pcols[i] < pcols[j]:
          num_matches += 1
          for col in range(pcols[i], pcols[j]):
            output[prows[i]][col] = 1
        if pcols[i] == pcols[j] and prows[i] < prows[j]:
          num_matches += 1
          for row in range(prows[i], prows[j]):
            output[row][pcols[i]] = 1
    # Draw the red plusses.
    for prow, pcol in zip(prows, pcols):
      output[prow][pcol] = grid[prow][pcol] = 0
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        output[prow + dr][pcol + dc] = grid[prow + dr][pcol + dc] = 2
    return grid, output, num_matches

  if width is None:
    width, height = common.randint(15, 16), common.randint(9, 18)
    num_plusses = common.randint(3, 5)
    expected_matches = num_plusses - 2 + common.randint(0, 1)
    while True:
      prows = [common.randint(1, height - 2) for _ in range(num_plusses)]
      pcols = [common.randint(1, width - 2) for _ in range(num_plusses)]
      if common.overlaps(prows, pcols, [3] * num_plusses, [3] * num_plusses):
        continue
      if common.some_abutted(prows, pcols, [3] * num_plusses, [3] * num_plusses):
        continue
      _, _, num_matches = draw()
      if num_matches == expected_matches: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=14, prows=[3, 3, 3, 9, 10],
               pcols=[3, 8, 13, 8, 2]),
      generate(width=15, height=10, prows=[1, 1, 5], pcols=[3, 10, 10]),
      generate(width=15, height=12, prows=[1, 4, 4, 9, 9],
               pcols=[8, 4, 11, 4, 11]),
  ]
  test = [
      generate(width=15, height=9, prows=[2, 4, 6, 6], pcols=[2, 7, 2, 10]),
  ]
  return {"train": train, "test": test}
