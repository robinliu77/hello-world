import re

original_settings_file_path = "/helloworld/settings.ini"
formatted_settings_file_path = "/helloworld/formatted_settings.ini"

# the sequence of the below fields is the output sequence to the file.
header = ""
product = ""
# hidpp Sorted by feature id
hidpp = ""
receiver = ""
shared = ""
runtime = ""
bug_tracker = ""

feature_id = ""
delimiter = "\n\n"
space = " "

with open(original_settings_file_path, "r") as file_input:

    original_settings = file_input.read()
    paragraph = original_settings.split("\n\n")
    product_dict = {}
    hidpp_dict = {}
    receiver_dict = {}
    shared_dict = {}
    runtime_dict = {}

    for i in range(len(paragraph)):
        if len(paragraph[i]) != 0:
            subsystem_name_available = re.search(r"\[[A-Z, \/, _]+\]", paragraph[i])
            feature_id_available = re.search(r"# Feature 0x(\w{4}) version \d{1,2}", paragraph[i])
            if subsystem_name_available is not None:
                subsystem_name = subsystem_name_available.group(0)
                if subsystem_name.startswith("[PRODUCT/FEATURES"):
                    if feature_id_available is not None:
                        feature_id = feature_id_available.group(0)
                        hidpp_dict[feature_id] = paragraph[i]
                    else:
                        feature_id_list = feature_id.split(" ")
                        version = feature_id_list[-1]
                        feature_id_list.remove(feature_id_list[-1])
                        feature_id_list.append(str(int(version) + 1))
                        feature_id = space.join(feature_id_list)
                        hidpp_dict[feature_id] = paragraph[i]
                elif subsystem_name.startswith("[PRODUCT") and subsystem_name.startswith("[PRODUCT/FEATURES") is False:
                    product_dict[subsystem_name.replace("]", "/")] = paragraph[i]
                elif subsystem_name.startswith("[RECEIVER"):
                    receiver_dict[subsystem_name.replace("]", "/")] = paragraph[i]
                elif subsystem_name.startswith("[SHARED"):
                    shared_dict[subsystem_name.replace("]", "/")] = paragraph[i]
                elif subsystem_name.startswith("[RUNTIME"):
                    runtime_dict[subsystem_name.replace("]", "/")] = paragraph[i]
                elif subsystem_name.startswith("[BUG_TRACKER"):
                    bug_tracker = paragraph[i]
                else:
                    print(subsystem_name)
            else:
                if feature_id_available is not None:
                    hidpp_dict[feature_id_available.group(0)] = paragraph[i]
                elif re.search(r"Python Test Harness", paragraph[i]) is not None:
                    header = paragraph[i]
                else:
                    print("NO SUBSYSTEM NAME")

product = delimiter.join(dict(sorted(product_dict.items())).values())
hidpp = delimiter.join(dict(sorted(hidpp_dict.items())).values())
receiver = delimiter.join(dict(sorted(receiver_dict.items())).values())
shared = delimiter.join(dict(sorted(shared_dict.items())).values())
runtime = delimiter.join(dict(sorted(runtime_dict.items())).values())

seq = (header, product, hidpp, receiver, shared, runtime, bug_tracker)
formatted_settings = delimiter.join(seq)

print(formatted_settings)

with open(formatted_settings_file_path, 'w') as output_file:
    output_file.write(formatted_settings)


