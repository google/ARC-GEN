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


def generate(spacing=None, start=None):
  """Returns input and output grids according to the given parameters.

  Args:
    spacing: The spacing of the input pixels.
    start: The start of the input pixels.
  """

  if spacing is None:
    spacing, start = common.randint(2, 4), common.randint(0, 1)

  grid, output = common.grids(15, 15)
  num = 0
  while start < 15:
    grid[start][start] = 1 if num < 3 else 0
    output[start][start] = 1 if num < 3 else 2
    start += spacing
    num += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(spacing=4, start=0),
      generate(spacing=2, start=1),
  ]
  test = [
      generate(spacing=3, start=0),
  ]
  return {"train": train, "test": test}
