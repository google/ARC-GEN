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
    colors: digits representing the colors to be used
  """

  if colors is None:
    values = common.random_colors(4)
    while True:
      colors = [common.choice(values) for _ in range(16)]
      if len(set(colors)) == 4: break

  grid, output = common.grid(4, 4), common.grid(8, 8)
  for i in range(16):
    grid[i // 4][i % 4] = colors[i]
    output[i // 4][i % 4] = colors[i]
    output[3 - i % 4][4 + i // 4] = colors[i]
    output[7 - i // 4][3 - i % 4] = colors[i]
    output[4 + i % 4][7 - i // 4] = colors[i]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 9, 1, 8, 8, 4, 1, 8, 4, 8, 8, 1, 1, 1, 1, 8]),
      generate(colors=[6, 2, 6, 2, 6, 6, 5, 5, 1, 1, 1, 2, 5, 1, 2, 1]),
      generate(colors=[6, 7, 7, 6, 7, 1, 6, 6, 9, 1, 6, 6, 9, 1, 6, 1]),
      generate(colors=[1, 1, 2, 1, 6, 6, 7, 6, 7, 6, 2, 1, 1, 6, 2, 6]),
      generate(colors=[4, 1, 9, 1, 1, 9, 1, 4, 9, 1, 4, 6, 4, 1, 6, 6]),
  ]
  test = [
      generate(colors=[4, 6, 4, 4, 4, 6, 4, 4, 7, 6, 7, 9, 9, 4, 9, 7]),
  ]
  return {"train": train, "test": test}
