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


def generate(xforms=None, color_dict=None, ins=None, outs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    xforms: The transforms to use.
    color_dict: The color dict to use.
    ins: The input colors to use.
    outs: The output colors to use.
  """

  if xforms is None:
    xforms = common.choices(["R", "L", "O"], common.randint(3, 4))
    if common.randint(0, 1): xforms[common.randint(0, len(xforms) - 1)] = "C"
    while True:  # Find color map that changes both, and adds 1+ new colors.
      icolors, ocolors = common.random_colors(2), common.random_colors(2)
      if icolors[0] == ocolors[0] or icolors[1] == ocolors[1]: continue
      if len(set(icolors + ocolors)) > 2: break
    color_dict = {icolors[0]: ocolors[0], icolors[1]: ocolors[1]}
    ins, outs = [], []
    for xform in xforms:
      if xform in ["L", "R"]:
        colors = common.random_colors(4)
        if common.randint(0, 1):
          ins.extend([colors[0], colors[0], colors[1], colors[1]])
          outs.extend([colors[2], colors[2], colors[3], colors[3]])
        else:
          ins.extend([colors[0], colors[1], colors[0], colors[1]])
          outs.extend([colors[2], colors[3], colors[2], colors[3]])
      if xform == "O":
        colors = common.random_colors(4)
        in_list, out_list = [colors[0]] * 4, [colors[2]] * 4
        in_list[common.randint(0, 3)] = colors[1]
        out_list[common.randint(0, 3)] = colors[3]
        ins.extend(in_list)
        outs.extend(out_list)
      if xform == "C":
        while True:
          ivals = [common.randint(0, 1) for _ in range(4)]
          ovals = [common.randint(0, 1) for _ in range(4)]
          if ivals == ovals: continue
          if len(list(set(ovals))) == 2 and len(list(set(ivals))) == 2: break
        ins.extend(icolors[val] for val in ivals)
        outs.extend(icolors[val] for val in ovals)

  def get_answer(xform, vals):
    if xform == "R":
      return [vals[2], vals[0], vals[3], vals[1]]
    if xform == "L":
      return [vals[1], vals[3], vals[0], vals[2]]
    if xform == "O":
      return [vals[1], vals[0], vals[3], vals[2]]
    return [color_dict[val] for val in vals]

  grid = common.grid(9, 3 * len(xforms) - 1)
  output = common.grid(2, 3 * len(xforms) - 1)
  for i, xform in enumerate(xforms):
    grid[3 * i][0] = ins[i * 4]
    grid[3 * i][1] = ins[i * 4 + 1]
    grid[3 * i + 1][0] = ins[i * 4 + 2]
    grid[3 * i + 1][1] = ins[i * 4 + 3]
    grid[3 * i][7] = outs[i * 4]
    grid[3 * i][8] = outs[i * 4 + 1]
    grid[3 * i + 1][7] = outs[i * 4 + 2]
    grid[3 * i + 1][8] = outs[i * 4 + 3]
    ans = get_answer(xform, ins[i * 4 : i * 4 + 4])
    grid[3 * i][3] = ans[0]
    grid[3 * i][4] = ans[1]
    grid[3 * i + 1][3] = ans[2]
    grid[3 * i + 1][4] = ans[3]
    ans = get_answer(xform, outs[i * 4 : i * 4 + 4])
    output[3 * i][0] = ans[0]
    output[3 * i][1] = ans[1]
    output[3 * i + 1][0] = ans[2]
    output[3 * i + 1][1] = ans[3]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(xforms="ORC", color_dict={3: 8, 7: 3},
               ins=[2, 4, 4, 4, 1, 1, 2, 2, 3, 7, 3, 3],
               outs=[8, 6, 8, 8, 5, 5, 4, 4, 3, 3, 3, 7]),
      generate(xforms="CRLO", color_dict={2: 5, 4: 8},
               ins=[2, 4, 4, 4, 5, 5, 9, 9, 2, 4, 2, 4, 1, 1, 1, 2],
               outs=[2, 4, 2, 4, 3, 3, 2, 2, 8, 3, 8, 3, 9, 9, 7, 9]),
  ]
  test = [
      generate(xforms="ORL", color_dict={},
               ins=[1, 1, 2, 1, 2, 2, 5, 5, 6, 6, 8, 8],
               outs=[4, 4, 3, 4, 3, 3, 1, 1, 7, 7, 4, 4]),
  ]
  return {"train": train, "test": test}
