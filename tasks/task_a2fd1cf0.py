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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    rows = common.sample(range(1, height - 2), 2)
    cols = common.sample(range(1, width - 2), 2)

  grid, output = common.hpwl(width, height, rows, cols, common.black(),
                             common.red(), common.green(), common.cyan())
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=15, rows=[1, 13], cols=[4, 10]),
      generate(width=16, height=10, rows=[7, 1], cols=[1, 11]),
      generate(width=14, height=12, rows=[1, 10], cols=[11, 4]),
  ]
  test = [
      generate(width=14, height=12, rows=[2, 10], cols=[1, 10]),
  ]
  return {"train": train, "test": test}
