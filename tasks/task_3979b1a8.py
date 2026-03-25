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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors.
  """

  if colors is None:
    colors = common.random_colors(3)

  grid, output = common.grid(5, 5), common.grid(10, 10)
  for r in range(10):
    for c in range(10):
      output[r][c] = colors[((r + 1) if r == c else max(r, c)) % 3]
  for g in [grid, output]:
    for r in range(5):
      for c in range(5):
        g[r][c] = colors[1]
    g[0][0] = g[0][4] = g[4][0] = g[4][4] = colors[2]
    g[1][2] = g[2][1] = g[2][2] = g[2][3] = g[3][2] = colors[0]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 3, 2]),
      generate(colors=[2, 8, 9]),
  ]
  test = [
      generate(colors=[9, 1, 5]),
  ]
  return {"train": train, "test": test}
