import pickle
import re
from collections import defaultdict

if __name__ == '__main__':
    # Load register prediction dictionary
    with open("bitwise_predictions_aes_core.pkl", "rb") as f:
        reg_dict = pickle.load(f)

    grouped = defaultdict(list)

    # Group by prefix before "_reg_"
    for key, value in reg_dict.items():
        match = re.match(r'(.*)_reg_.*', key)
        print(f"Endpoint: {key:} -> {value:.6f}")
        if match:
            prefix = match.group(1)
            grouped[prefix].append(value)

    # Get max value per group
    result = {prefix: max(vals) for prefix, vals in grouped.items()}

    # Annotate Verilog
    with open("aes_cipher_top.v", "r") as fin:
        lines = fin.readlines()

    new_lines = []
    for line in lines:
        line_clean = line.replace('\t', ' ').strip()
        match = re.match(r'^(reg|wire)\s*(\[[^\]]+\])?\s+(.+);', line_clean)
        if match:
            decl_type, width, var_str = match.groups()
            vars_list = [v.strip() for v in var_str.split(',')]

            # Check if any of these vars belong to a group
            for var in vars_list:
                for prefix, slack in result.items():
                    if var.startswith(prefix):
                        print(f"Annotated: {var:<15} -> Worst Slack = {slack:.6f}")
                        comment = f"// Worst Slack = {slack:.6f} ({var})\n"
                        new_lines.append(comment)
                        break

        new_lines.append(line)

    with open("aes_cipher_top_annotated.v", "w") as fout:
        fout.writelines(new_lines)
