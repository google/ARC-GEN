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


def generate(width=None, height=10):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
  """
  if width is None:
    width = common.randint(2, 10)

  grid, output = common.bounce(width, height, common.black(), common.cyan(),
                               common.blue())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2),
      generate(width=3),
      generate(width=4),
  ]
  test = [
      generate(width=5),
  ]
  return {"train": train, "test": test}
