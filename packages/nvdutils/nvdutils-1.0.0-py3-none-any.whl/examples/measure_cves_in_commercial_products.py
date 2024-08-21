import json
from tqdm import tqdm
from collections import defaultdict
from pathlib import Path

from nvdutils.core.loaders.json_loader import JSONFeedsLoader
from nvdutils.types.options import CVEOptions, ConfigurationOptions

cve_options = CVEOptions(config_options=ConfigurationOptions(has_config=True, has_vulnerable_products=True))

loader = JSONFeedsLoader(data_path='~/.nvdutils/nvd-json-data-feeds',
                         options=cve_options,
                         verbose=True)

# Populate the loader with CVE records
loader.load()

cna_vendor_cve = 0
cna_vendor_match = 0
cna_open_source_match = 0
cve_is_in_open_source = 0
cve_is_in_vendor = 0
cve_is_in_unknown = 0
cna_vendor_names = defaultdict(lambda: defaultdict(set))
cna_vendor_names_matches = defaultdict(lambda: defaultdict(set))
open_source_vendor_names = defaultdict(lambda: defaultdict(set))


for cve_id, cve in tqdm(loader.records.items(), desc=""):
    if cve.source not in loader.cnas:
        continue

    cna_vendor_cve += 1

    vuln_products = cve.get_vulnerable_products()

    vendors = set()
    owners = set()

    for commit in cve.get_commit_references(vcs='github'):
        owners.add(commit.owner)

    for product in vuln_products:
        vendors.add(product.vendor)

    overlap_vendors = vendors.intersection(loader.cnas[cve.source].scope.keys())
    overlap_owners = owners.intersection(loader.cnas[cve.source].get_owners())

    if overlap_owners:
        cna_open_source_match += 1
        cve_is_in_open_source += 1

    elif overlap_vendors:
        cna_vendor_match += 1

        for vendor_name in overlap_vendors:
            # cna_vendor_names_matches[cve.source][vendor].add(cve_id)
            vendor = loader.cnas[cve.source].scope[vendor_name]
            if not vendor.is_vendor() and vendor.is_open_source():
                # open_source_vendor_names[cve.source][vendor].add(cve_id)
                cve_is_in_open_source += 1
                break
        else:
            cve_is_in_vendor += 1
    else:
        cve_is_in_unknown += 1

    #else:
    #    for vendor in vendors:
    #        cna_vendor_names[cve.source][vendor].add(cve_id)
    #        if '_project' in vendor.lower():
    #            open_source_vendor_names[cve.source][vendor].add(cve_id)

print(f"CVEs with CNA vendor: {cna_vendor_cve}")
print(f"CVEs with CNA open source match: {cna_open_source_match}")
print(f"CVEs with CNA vendor match: {cna_vendor_match}")
print(f"CVEs in open source projects: {cve_is_in_open_source}")
print(f"CVEs in commercial product: {cve_is_in_vendor}")
print(f"CVEs in unknown software: {cve_is_in_unknown}")
#print(f"CNAs with CVEs: {len(cna_vendor_names)}")
#print(f"No match CVEs: {cna_vendor_names}")
#print(f"CNAs with vendor name match: {len(cna_vendor_names_matches)}")
#print(f"Open source projects: {sum([len(v) for v in open_source_vendor_names.values()])}")
