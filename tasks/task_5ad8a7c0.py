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


def generate(cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: The columns of the red pixels.
  """

  if cols is None:
    while True:
      cols = [common.randint(-1, 2) for _ in range(4)]
      if max(cols) != -1: break

  grid, output = common.grids(6, 4)
  for r, col in enumerate(cols):
    if col == -1: continue
    output[r][col] = output[r][5 - col] = grid[r][col] = grid[r][5 - col] = 2
    if col != max(cols): continue
    for c in range(col, 3):
      output[r][c] = output[r][5 - c] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[0, -1, -1, 0]),
      generate(cols=[0, 1, 2, 1]),
      generate(cols=[-1, 1, 0, 1]),
      generate(cols=[2, 1, 0, 1]),
      generate(cols=[0, 1, 1, 0]),
  ]
  test = [
      generate(cols=[0, 1, -1, 0]),
  ]
  return {"train": train, "test": test}
