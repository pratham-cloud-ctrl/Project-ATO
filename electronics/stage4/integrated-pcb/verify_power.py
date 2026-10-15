"""Independent decimal energy/current audit of the additive populated budget."""
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    result = json.loads((HERE/'power-overlay.json').read_text())
    checks = 0
    def check(value, reason):
        nonlocal checks
        checks += 1
        assert value, reason
    def close(actual, expected, reason):
        check(abs(D(str(actual))-expected) < D('1e-11'), reason)
    for path, digest in result['source_sha256_lf'].items():
        check(hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==digest, path)
    carrier = json.loads((ROOT/'electronics/stage4/controller-carrier/connectivity.json').read_text())
    old = json.loads((ROOT/'electronics/stage4/power-study/budget-results.json').read_text())
    transport = json.loads((ROOT/'electronics/stage4/transport-study/input-results.json').read_text())['power_overlay']
    parts = {p['ref']:p for p in carrier['parts']}
    check(len(parts)==68, '68 actual carrier components')
    check(sum(p['kind']=='module' for p in parts.values())==1, 'one module')
    check(sum('165' in p['value'] for p in parts.values())==4, 'four serializers')
    bias_refs = {r for r,p in parts.items() if r.startswith('R') and p['value']=='10k'}
    check(bias_refs=={'R2'}|{f'R{x}' for x in range(100,140)}, 'reset bias plus forty GPIO biases')
    check(set(result['bias_resistors'])==bias_refs, 'all biases allocated')
    close(result['allocations_A']['all_41_biases_opposed_A'], D(41)*D('3.3')/D(10000), 'bias sum')
    close(result['allocations_A']['previous_passive_dynamic_contingency_A'],
          D(str(old['inventory']['rails']['HOST_3V3']['passive_dynamic_output_load_contingency_A'])), 'prior contingency retained')
    close(result['HOST_3V3_new_cap_A'], D('.160'), 'revised cap')
    check(result['allocated_A'] < result['HOST_3V3_new_cap_A'], 'positive allocation headroom')
    check(D(str(result['allocations_A']['BT40F_module_declared_A']))==D('.060'), 'module conditional allocation')
    check(result['module_and_serializer_currents_are_design_allocations'], 'not measured maxima')
    power = D(str(transport['active_W'])) + (D('.160')-D('.080'))*D('3.3')/D('.8')*D('7.4')/D('6.9')
    close(result['active_W'], power, 'battery energy balance including diode loss')
    close(result['runtime_h']*result['active_W'], D('15.392'), 'runtime times power equals usable energy')
    cap = D('48.5e-6')
    close(result['carrier_capacitance_F'], cap, 'all seven carrier bypass capacitors')
    close(result['carrier_energy_J'], cap*D('3.3')**2/2, 'capacitor energy')
    close(result['carrier_energy_plus20percent_J'], cap*D('3.3')**2/2*D('1.2'), 'capacitance margin')
    check(not result['compact_implanted_thermal_2K_earned'], 'compact thermal failure retained')
    check(not result['converter_stability_inrush_efficiency_and_physical_execution_measured'], 'unmeasured hardware retained')
    print(f'Integrated independent power audit: {checks} checks passed')


if __name__ == '__main__': main()
