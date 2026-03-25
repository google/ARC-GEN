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
    colors: The colors of the pixels.
  """

  if colors is None:
    colors = common.random_colors(4)

  grid, output = common.grids(4, 4)
  for i, color in enumerate(colors):
    output[3 * (i // 2)][3 * (i % 2)] = grid[i // 2 + 1][i % 2 + 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 6, 8, 3]),
      generate(colors=[3, 4, 7, 6]),
  ]
  test = [
      generate(colors=[2, 3, 4, 9]),
  ]
  return {"train": train, "test": test}
