"""Verify Stage2 reproducibility and consistency; no efficacy qualification."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
from urllib.parse import unquote
from pypdf import PdfReader
from run_architecture_budgets import calculate, equivalent

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/stage2'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    checks=[]
    config=json.loads((DOC/'system-design.json').read_text(encoding='utf-8'))
    acquisition=json.loads((DOC/'acquisition-budget-inputs.json').read_text(encoding='utf-8'))
    timing=json.loads((DOC/'timing-budget-inputs.json').read_text(encoding='utf-8'))
    contracts=json.loads((DOC/'control-contracts.json').read_text(encoding='utf-8'))
    stimulation=json.loads((DOC/'stimulation-budget-inputs.json').read_text(encoding='utf-8'))
    calculated=calculate()
    previous=json.loads((ROOT/'results/stage2/budget-summary.json').read_text(encoding='utf-8'))
    assert equivalent(calculated,previous),'Budget result drift'
    checks.append('Committed analytical results reproduce at1e-10 relative/1e-12 absolute tolerance; gates exact')
    assert config['recording']['sampled_differential_streams']==acquisition['channels']['sampled_differential_streams']
    assert config['recording']['sample_rate_per_stream_hz']==timing['parameters']['raw_sample_rate_per_stream']['value']
    assert config['stimulation']['independent_sources']==timing['parameters']['independent_stim_sources']['value']==2
    assert config['compute']['clock_hz']==acquisition['compute']['application_clock_Hz']==128000000
    assert abs(config['compute']['allocated_cycles_per_second']-calculated['compute_and_transport']['analytical_cycles_per_s'])<1
    assert sum(acquisition['storage']['RAM_allocations_bytes'].values())==calculated['compute_and_transport']['application_ram_allocated_bytes']
    assert stimulation['parameters']['charge_ceiling_per_phase']['value']==config['stimulation']['delivery_charge_ceiling_C']
    assert stimulation['parameters']['command_charge_ceiling_per_phase']['value']==config['stimulation']['command_charge_ceiling_C']
    checks.append('Integrated and audited acquisition/timing inputs agree on streams/rate/clock/sources/cycles/RAM')
    c=calculated['compute_and_transport']
    assert c['128MHz_60pct_budget_pass'] and c['20pct_ram_headroom_gate_pass']
    assert not c['64MHz_60pct_budget_pass'] and not c['two_second_raw4k_fits_physical_ram']
    assert c['monitor_ADC_utilization']<1 and c['monitor_SPI_utilization_with_overhead']<1
    assert c['neural_scan_occupancy_fraction']<1
    checks.append('Selected compute/transport margins and explicit64MHz/raw-RAM failures preserved')
    ids=[r['id'] for r in contracts['contracts']]
    assert len(ids)==len(set(ids))==11
    assert all(c['fields'] for c in contracts['contracts'])
    allowed={r['verification_id'] for r in csv.DictReader((ROOT/'docs/stage1/verification-matrix.csv').open(encoding='utf-8'))}
    assert set(contracts['future_verification_links'])<=allowed
    progress=list(csv.DictReader((DOC/'verification-progress.csv').open(encoding='utf-8')))
    assert set(r['verification_id'] for r in progress)<=allowed
    assert 'Partially' in next(r['stage2_status'] for r in progress if r['verification_id']=='S1-V-204')
    checks.append('Eleven control contracts and scoped progress map to Stage1 checks; identified authority remains open')
    by_id={r['id']:r for r in calculated['profiles']}
    assert by_id['motor_reference']['all_selected_continuous_gates_pass']
    assert by_id['pressure_reference']['all_selected_continuous_gates_pass']
    assert not by_id['pressure_reference']['motor_observation_gates']['global_coverage']
    assert not by_id['pressure_high_current_stress']['all_selected_continuous_gates_pass']
    assert not by_id['cartesian_max_rejected']['selected_continuous_gates']['joint_command_charge']
    assert not by_id['cartesian_max_rejected']['selected_continuous_gates']['delivery_charge_with_uncertainty']
    assert not calculated['telemetry']['raw4k_1M_target_pass']
    assert not calculated['quiet_noise'][1]['quiet_10dB_gate_pass']
    assert all(not r['passes25ms_chosen_deadline'] for r in calculated['reactive_frame_wait'][:3])
    checks.append('Nominal conditional gates and noise/blanking/charge/power/timing/telemetry failures preserved')
    assert abs(calculated['fast_chain_ms']-11.85)<1e-9
    assert abs(timing['latency_analysis']['total_fast_unframed_bound_s']*1000-calculated['fast_chain_ms'])<1e-9
    assert abs(by_id['pressure_reference']['blanked_fraction_with_preguard']-.648)<1e-10
    assert any(row['Rtheta_K_per_W']==40 and not row['chosen2K_gate_pass'] for row in calculated['thermal_sensitivity'])
    assert abs(calculated['reservoir']['droop_V']-40/33)<1e-10
    checks.append('Timing update, periodic mask union, thermal sensitivity and reservoir units agree')
    assert calculated['filters']['archive_0p5dB_passband_gate_pass']
    assert calculated['filters']['archive60dB_stopband_gate_pass']
    assert calculated['filters']['fast_band_max_ideal_group_delay_ms']<2
    assert by_id['pressure_reference']['archive_FIR_invalid_fraction_any_raw_invalid_rule']==1
    assert abs(by_id['motor_reference']['archive_FIR_invalid_fraction_any_raw_invalid_rule']-.364)<1e-12
    expansion=next(row for row in calculated['channel_scaling'] if row['streams']==32)
    assert not expansion['CPU60pct_gate_pass'] and not expansion['RAM20pct_headroom_gate_pass']
    assert expansion['total_body_ports_including18_output']==53
    checks.append('Numerical FIR/ideal delay, archive mask propagation and32-stream resource rejection agree')
    source_count=0
    for filename,idfield in [('electrical-source-audit.csv','claim_id'),('biological-envelope-audit.csv','parameter_id'),('system-source-audit.csv','source_id')]:
        rows=list(csv.DictReader((DOC/filename).open(encoding='utf-8-sig',newline='')))
        if idfield not in rows[0]:idfield=list(rows[0])[0]
        ids=[r[idfield] for r in rows]
        assert len(ids)==len(set(ids))
        assert all(None not in r and r[idfield] for r in rows)
        source_count+=len(rows)
    checks.append(f'{source_count} parameter/provenance audit rows have unique IDs and valid CSV structure')
    links=0
    for filename in DOC.glob('*.md'):
        content=filename.read_text(encoding='utf-8')
        assert content.count('```')%2==0
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',content):
            target=target.strip('<>')
            if target.startswith(('https://','http://','#','mailto:')):continue
            assert (filename.parent/unquote(target.split('#')[0])).resolve().exists(),(filename,target)
            links+=1
    checks.append(f'{links} local Stage2 Markdown links resolve; fences balance')
    cad=json.loads((ROOT/'cad/stage2/allocation-checks.json').read_text(encoding='utf-8'))
    native=json.loads((ROOT/'cad/stage2/freecad-checks.json').read_text(encoding='utf-8'))
    assert cad['ports']==36==config['mechanical']['body_feedthrough_ports']
    assert cad['assembly_solid_count']==len(cad['parts'])==native['step_import_solid_count']==native['reopened_native_solid_count']==80
    assert all(r['valid_BRep'] and r['volume_mm3']>0 for r in cad['parts'])
    assert all(r['overlap_mm3']<1e-6 for r in cad['pairwise_major_solids_intersection_checks'])
    assert all(r['metal_can_overlap_mm3']<1e-6 for r in cad['interface_can_checks'])
    assert abs(native['volume_error_mm3'])<1e-4
    checks.append('Recorded local CAD execution:80 valid solids,36 ports, nominal major/can-port checks and FreeCAD volume round-trip')
    pdf=ROOT/'output/pdf/ATO_stage2_architecture_budgets.pdf'
    pages=PdfReader(pdf).pages
    assert len(pages)==8
    for i,page in enumerate(pages,1):
        text=page.extract_text()
        assert len(text)>750 and '\ufffd' not in text
        assert 'ANALYTICAL DESIGN PROPOSAL' in text
        assert f'{i} / 8' in text
    review=json.loads((ROOT/'provenance/stage2-review.json').read_text(encoding='utf-8'))
    assert review['pdf_visual_review']['sha256']==sha(pdf)
    assert review['pdf_visual_review']['page_count']==8
    for name in ['ATO_stage2_allocation.step','ATO_stage2_allocation.FCStd']:
        assert review['cad_artifacts_sha256'][name]==sha(ROOT/'cad/stage2'/name)
    for name in ['recording-compute','artifact-timing','compliance-monitor','power-envelope','thermal-envelope','mechanical-allocation']:
        assert (DOC/'figures'/f'{name}.png').stat().st_size>10000
        assert '<svg' in (DOC/'figures'/f'{name}.svg').read_text(encoding='utf-8')
    checks.append('Eight-page PDF numbering/text, six SVG/PNG figure pairs and review/native hashes match')
    return {'date':'2026-10-08','stage':'Stage2 quantitative architecture package',
        'scope':'Reproducibility and consistency; CAD geometry executed locally and tied to hashes; no hardware/biological qualification',
        'checks':checks,'parameter_audit_rows':source_count,'control_contract_count':11,
        'cad_solid_count':80,'pdf_pages':8,
        'pending':'S1-V-204 identified response/functional reachability remains Stage3; complete circuits/firmware Stage4 and populated CAD Stage5 remain pending'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-receipt',action='store_true');args=parser.parse_args()
    receipt=verify()
    if args.write_receipt:
        (ROOT/'provenance/stage2-verification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
