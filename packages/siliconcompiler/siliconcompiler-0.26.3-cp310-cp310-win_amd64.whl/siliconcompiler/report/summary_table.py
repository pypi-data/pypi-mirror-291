import pandas

from siliconcompiler.report.utils import _collect_data, _get_flowgraph_path
from siliconcompiler.tools._common import get_tool_task


def _show_summary_table(chip, flow, flowgraph_nodes, show_all_indices):
    '''
    Prints the end of run summary table
    '''

    # Display data
    pandas.set_option('display.max_rows', 500)
    pandas.set_option('display.max_columns', 500)
    pandas.set_option('display.width', 100)

    nodes, _, metrics, metrics_unit, metrics_to_show, _ = \
        _collect_data(chip, flow, flowgraph_nodes)

    selected_tasks = \
        _get_flowgraph_path(chip, flow, flowgraph_nodes, only_include_successful=True)

    # only report tool based steps functions
    for (step, index) in flowgraph_nodes.copy():
        if get_tool_task(chip, step, index, flow=flow)[0] == 'builtin':
            del flowgraph_nodes[flowgraph_nodes.index((step, index))]

    if show_all_indices:
        nodes_to_show = nodes
    else:
        nodes_to_show = [n for n in nodes if n in selected_tasks]

    # Custom reporting modes
    paramlist = []
    for item in chip.getkeys('option', 'param'):
        paramlist.append(item + "=" + chip.get('option', 'param', item))

    if paramlist:
        paramstr = ', '.join(paramlist)
    else:
        paramstr = "None"

    colwidth = 8  # minimum col width
    row_labels = [' ' + metric for metric in metrics_to_show]
    column_labels = [f'{step}{index}'.center(colwidth)
                     for step, index in nodes_to_show]
    column_labels.insert(0, 'units')

    data = []
    for metric in metrics_to_show:
        row = []
        row.append(metrics_unit[metric])
        for node in nodes_to_show:
            value = metrics[node][metric]
            if value is None:
                value = '---'
            value = ' ' + value.center(colwidth)
            row.append(value)
        data.append(row)

    info_list = ["SUMMARY:\n",
                 "design : " + chip.design,
                 "params : " + paramstr,
                 "jobdir : " + chip.getworkdir()]

    pdk = chip.get('option', 'pdk')
    if pdk:
        info_list.extend([
            f"foundry : {chip.get('pdk', pdk, 'foundry')}",
            f"process : {pdk}"])
    else:
        fpga_partname = chip.get('fpga', 'partname')
        if fpga_partname:
            info_list.append(f"partname : {fpga_partname}")

    libraries = set()
    for val, step, index in chip.schema._getvals('asic', 'logiclib'):
        if not step or (step, index) in flowgraph_nodes:
            libraries.update(val)
    if libraries:
        info_list.append(f"targetlibs : {' '.join(libraries)}")

    info = '\n'.join(info_list)

    print("-" * 135)
    print(info, "\n")

    df = pandas.DataFrame(data, row_labels, column_labels)
    if not df.empty:
        print(df.to_string())
    else:
        print(' No metrics to display!')
    print("-" * 135)
