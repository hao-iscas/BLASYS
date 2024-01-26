# Date: 2024-1-16
# Description: Plot the summary graph between BLASYS and OPTIMALALS methods

import pandas as pd
import sys
import os
import matplotlib.pyplot as plt


def load_results_csv(result_path):
    '''
        result_path: path of results given
    '''
    assert os.path.isfile(result_path) and result_path.endswith('.csv')
    
    df = pd.read_csv(result_path)

    metric_list = df['Metric'].to_list()
    area_list = df['Area(um^2)'].to_list()
    name_list = df['Name'].to_list()
    power_list = df['Power(uW)'].to_list()
    delay_list = df['Delay(ns)'].to_list()
    
    transform_per = lambda v_list: [v / v_list[0] for v in v_list]
    transform_per_h = lambda v_list: [v * 100 for v in v_list]

    area_list = transform_per_h(transform_per(area_list))
    power_list = transform_per_h(transform_per(power_list))
    delay_list = transform_per_h(transform_per(delay_list))
    metric_list = transform_per_h(metric_list)

    return name_list, metric_list, area_list, power_list, delay_list

def plot_scatter(results_path_label_dict, dot_label_dict, scatter_suptitle):
    '''
        {label: results_path}
        dot_label_dict is in format of {label: (color, size)}
    '''
    name_l_dict, area_l_dict, metric_l_dict, power_l_dict, delay_l_dict = {}, {}, {}, {}, {}
    # area_t_list, metric_t_list, power_t_list, delay_t_list = [], [], [], []
    # colors, scales = [], []

    for l, res_path in results_path_label_dict.items():
        res = load_results_csv(res_path)
        name_l_dict[l] = res[0]
        metric_l_dict[l] = res[1]
        # metric_t_list += res[1]
        area_l_dict[l] = res[2]
        # area_t_list += res[2]
        power_l_dict[l] = res[3]
        # power_t_list += res[3]
        delay_l_dict[l] = res[4]
        # delay_t_list += res[4]
    
        # assert l in dot_label_dict.keys()
        # colors += [dot_label_dict[l][0] * len(res[0])]
        # scales += [dot_label_dict[l][1] * len(res[0])]

    # 3 plots in one line (1 area, 1 power. 1 delay)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.suptitle(scatter_suptitle)

    # ax1 is QoR-Area scatter (x for QoR, y for Area)
    ax1.set_xlabel('QoR (Hamming Distance) %')
    ax1.set_ylabel('Area Utilisation %')
    for l in metric_l_dict.keys():
        assert l in area_l_dict.keys()
        ax1.scatter(metric_l_dict[l], area_l_dict[l], c=dot_label_dict[l][0], s=dot_label_dict[l][1], label=l, alpha=0.8)
    ax1.legend()
    
    # ax2 is QoR-Power scatter (x for QoR, y for Power)
    ax2.set_xlabel('QoR (Hamming Distance) %')
    ax2.set_ylabel('Power Utilisation %')
    for l in metric_l_dict.keys():
        assert l in power_l_dict.keys()
        ax2.scatter(metric_l_dict[l], power_l_dict[l], c=dot_label_dict[l][0], s=dot_label_dict[l][1], label=l, alpha=0.8)
    ax2.legend()

    # ax3 is QoR-Delay scatter (x for QoR, y for Delay)
    ax3.set_xlabel('QoR (Hamming Distance) %')
    ax3.set_ylabel('Delay Percentage %')
    for l in metric_l_dict.keys():
        assert l in delay_l_dict.keys()
        ax3.scatter(metric_l_dict[l], delay_l_dict[l], c=dot_label_dict[l][0], s=dot_label_dict[l][1], label=l, alpha=0.8)
    ax3.legend()

    # fig.savefig(os)
    plt.show()

if __name__ == '__main__':
    assert len(sys.argv) == 4

    # argv[1] => list of labels
    # argv[2] => list of results_csv_paths
    # argv[3] => list of dot labels (g0 => color 'g' and scale candidate [0])
    # argv[4] => scatter_suptitle
    labels = sys.argv[1].strip().split(',')
    csv_paths = sys.argv[2].strip().split(',')
    dot_pars = sys.argv[3].strip().split(',')
    scatter_sup_title = sys.argv[4]

    scales_candidate = [20 * 3**i for i in range(10)]
    results_path_label_dict = {l: csv_path for l, csv_path in zip(labels, csv_paths)}
    dot_label_dict = {l: (dot_par[0], scales_candidate[int(dot_par[1:])]) for l, dot_par in zip(labels, dot_pars)}

    plot_scatter(results_path_label_dict, dot_label_dict, scatter_sup_title)
