#include "ato_runtime.h"
#include <float.h>
#include <limits.h>
#include <math.h>
#include <string.h>

_Static_assert(sizeof(float)==4 && FLT_RADIX==2 && FLT_MANT_DIG==24,
               "SBP wire protocol requires binary32 float");
_Static_assert(sizeof(ato_fault_record)==16, "fault record allocation");
_Static_assert(sizeof(ato_runtime)<2048, "bounded core state");

static void changed(ato_runtime *r) { ++r->output.generation; }
static void outputs_off(ato_runtime *r) {
    r->output.request_mask=0;
    r->output.want_mask=0;
    r->output.armed=0;
    r->output.diagnostic_capture=0;
    r->output.current_ua[0]=0;
    r->output.current_ua[1]=0;
    r->phase_ready=0;
    r->pending_actions=0;
    r->state=ATO_STATE_IDLE;
    changed(r);
}
void ato_runtime_trip(ato_runtime *r, ato_runtime_fault reason, uint16_t detail,
                      uint64_t now_us) {
    ato_fault_record *f;
    if (!r) return;
    /* A backwards timestamp is recorded at the last trusted local time. */
    if (now_us>=r->now_us) r->now_us=now_us;
    if (reason==ATO_FAULT_NONE) reason=ATO_FAULT_HARD_TRIP;
    r->sticky_fault=(uint16_t)reason;
    r->route_valid=0;
    r->route_pending=0;
    outputs_off(r);
    f=&r->faults[r->fault_head];
    f->at_us=r->now_us;
    f->event_id=r->plan.event_id;
    f->reason=(uint16_t)reason;
    f->detail=detail;
    r->fault_head=(uint8_t)((r->fault_head+1u)%ATO_FAULT_LOG_CAPACITY);
    if (r->fault_count<ATO_FAULT_LOG_CAPACITY) ++r->fault_count;
    if (r->fault_total<UINT32_MAX) ++r->fault_total;
}
static bool clock_ok(ato_runtime *r, uint64_t now_us) {
    if (!r) return false;
    if (now_us<r->now_us) {
        ato_runtime_trip(r,ATO_FAULT_CLOCK,1,r->now_us);
        return false;
    }
    r->now_us=now_us;
    return true;
}
static bool add_time(uint64_t now, uint64_t delta, uint64_t *answer) {
    if (delta>UINT64_MAX-now) return false;
    *answer=now+delta;
    return true;
}
static bool shifted_time(uint64_t peer, int64_t offset, uint64_t *local) {
    if (offset>=0) return add_time(peer,(uint64_t)offset,local);
    if (offset==INT64_MIN || peer<(uint64_t)(-offset)) return false;
    *local=peer-(uint64_t)(-offset);
    return true;
}
static bool health_ok(const ato_runtime *r) {
    return (r->health&ATO_REQUIRED_HEALTH)==ATO_REQUIRED_HEALTH;
}
static bool quiet(const ato_runtime *r) {
    return r->quiet_mask==3u && !r->timer_active_mask && !r->run_mask
           && !r->output.request_mask;
}
static bool pressure_fresh(const ato_runtime *r, uint64_t now) {
    return r->pressure_valid && now>=r->pressure_oldest_us
           && now-r->pressure_oldest_us<=2000000u;
}
static bool lease_fresh(const ato_runtime *r, uint64_t now) {
    return r->command_seen && now<r->lease_deadline_us;
}
static bool admitted(const ato_runtime *r, uint64_t now) {
    return !r->sticky_fault && r->output.armed && r->config_valid
        && r->sample_seen && health_ok(r) && lease_fresh(r,now)
        && (r->mode!=ATO_MODE_PRESSURE || pressure_fresh(r,now));
}
void ato_runtime_init(ato_runtime *r, uint64_t now_us) {
    if (!r) return;
    memset(r,0,sizeof(*r));
    r->now_us=now_us;
    r->mode=ATO_MODE_OBSERVE;
    ato_runtime_trip(r,ATO_FAULT_BOOT,0,now_us);
}
bool ato_runtime_configure(ato_runtime *r, uint32_t epoch, bool readback_ok,
                           uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!epoch || epoch==r->config_epoch || !readback_ok || !quiet(r)
        || r->state!=ATO_STATE_IDLE) {
        r->config_valid=0;
        ato_runtime_trip(r,ATO_FAULT_CONFIG,1,now_us);
        return false;
    }
    r->config_epoch=epoch;
    r->config_valid=1;
    r->sample_seen=0;
    r->last_capture_id=0;
    r->command_seen=0;
    r->event_seen=0;
    r->raw_queue_used=0;
    r->normal_queue_used=0;
    ato_runtime_trip(r,ATO_FAULT_CONFIG,0,now_us);
    return true;
}
void ato_runtime_health(ato_runtime *r, uint16_t health, uint8_t quiet_mask,
                        uint8_t timer_active_mask, uint8_t run_mask,
                        uint64_t now_us) {
    if (!clock_ok(r,now_us)) return;
    r->health=health;
    r->quiet_mask=(uint8_t)(quiet_mask&3u);
    r->timer_active_mask=(uint8_t)(timer_active_mask&3u);
    r->run_mask=(uint8_t)(run_mask&3u);
    if (!health_ok(r) && (r->output.armed || r->state!=ATO_STATE_IDLE))
        ato_runtime_trip(r,ATO_FAULT_HEALTH,
                          (uint16_t)(ATO_REQUIRED_HEALTH&~health),now_us);
}
bool ato_runtime_session(ato_runtime *r, uint32_t epoch, uint32_t calibration_id,
                         int64_t offset_lo_us, int64_t offset_hi_us,
                         uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!epoch || !calibration_id || offset_lo_us>offset_hi_us
        || offset_lo_us < -1000000000000LL || offset_hi_us>1000000000000LL
        || offset_hi_us-offset_lo_us>1000 || r->state!=ATO_STATE_IDLE) {
        r->session_valid=0;
        r->pressure_valid=0;
        ato_runtime_trip(r,ATO_FAULT_PACKET,1,now_us);
        return false;
    }
    r->session_epoch=epoch;
    r->calibration_id=calibration_id;
    r->clock_offset_lo_us=offset_lo_us;
    r->clock_offset_hi_us=offset_hi_us;
    r->session_valid=1;
    r->pressure_valid=0;
    r->pressure_seen=0;
    ato_runtime_trip(r,ATO_FAULT_CONFIG,2,now_us);
    return true;
}
static uint16_t get16(const uint8_t *b) {
    return (uint16_t)((uint16_t)b[0]|((uint16_t)b[1]<<8));
}
static uint32_t get32(const uint8_t *b) {
    return (uint32_t)b[0]|((uint32_t)b[1]<<8)|((uint32_t)b[2]<<16)
           |((uint32_t)b[3]<<24);
}
static uint64_t get64(const uint8_t *b) {
    return (uint64_t)get32(b)|((uint64_t)get32(b+4)<<32);
}
static float getfloat(const uint8_t *b) {
    uint32_t bits=get32(b);
    float f;
    memcpy(&f,&bits,sizeof(f));
    return f;
}
uint32_t ato_runtime_crc32(const uint8_t *bytes, size_t length) {
    uint32_t crc=UINT32_MAX;
    size_t i;
    unsigned bit;
    if (!bytes && length) return 0;
    for (i=0;i<length;++i) {
        crc^=bytes[i];
        for (bit=0;bit<8;++bit)
            crc=(crc>>1)^((0u-(crc&1u))&0xedb88320u);
    }
    return ~crc;
}
static bool bad_packet(ato_runtime *r, uint16_t detail, uint64_t now) {
    r->pressure_valid=0;
    ato_runtime_trip(r,ATO_FAULT_PACKET,detail,now);
    return false;
}
bool ato_runtime_sbp(ato_runtime *r, const uint8_t *p, size_t length,
                     uint64_t now_us) {
    uint32_t sequence,advance;
    uint64_t first,last,extracted,oldest_local,last_latest,extract_earliest;
    float pressure,uncertainty;
    if (!clock_ok(r,now_us)) return false;
    if (!p || length!=ATO_SBP_PACKET_BYTES) return bad_packet(r,2,now_us);
    if (get32(p+52)!=ato_runtime_crc32(p,52)) return bad_packet(r,3,now_us);
    if (p[0]!='A' || p[1]!='T' || p[2]!=1 || p[3]!=2
        || get16(p+36)!=12 || get16(p+38)!=0)
        return bad_packet(r,4,now_us);
    if (!r->session_valid || get32(p+4)!=r->session_epoch)
        return bad_packet(r,5,now_us);
    sequence=get32(p+8);
    advance=sequence-r->pressure_sequence;
    if (r->pressure_seen && (!advance || advance>=0x80000000u))
        return bad_packet(r,6,now_us);
    first=get64(p+12); last=get64(p+20); extracted=get64(p+28);
    if (first>last || last>extracted
        || !shifted_time(first,r->clock_offset_lo_us,&oldest_local)
        || !shifted_time(last,r->clock_offset_hi_us,&last_latest)
        || !shifted_time(extracted,r->clock_offset_lo_us,&extract_earliest)
        || last_latest>now_us || extract_earliest>now_us
        || oldest_local>now_us || now_us-oldest_local>2000000u)
        return bad_packet(r,7,now_us);
    /* Compare oldest support, matching the prior transport contract. */
    if (r->pressure_seen && first<=r->pressure_newest_peer_us)
        return bad_packet(r,8,now_us);
    pressure=getfloat(p+40); uncertainty=getfloat(p+44);
    if (!isfinite(pressure) || !isfinite(uncertainty)
        || pressure<50.0f || pressure>250.0f
        || uncertainty<0.0f || uncertainty>50.0f
        || get32(p+48)!=r->calibration_id)
        return bad_packet(r,9,now_us);
    r->pressure_sequence=sequence;
    r->pressure_newest_peer_us=first;
    r->pressure_oldest_us=oldest_local;
    r->pressure_valid=1;
    r->pressure_seen=1;
    /* Receipt establishes support, never clears a sticky inhibition. */
    return true;
}
bool ato_runtime_command(ato_runtime *r, ato_mode mode, uint32_t epoch,
                         uint32_t sequence, uint32_t lease_us,
                         uint64_t now_us) {
    uint32_t max_lease,advance;
    uint64_t deadline;
    if (!clock_ok(r,now_us)) return false;
    max_lease=mode==ATO_MODE_PRESSURE ? 3000000u :
              mode==ATO_MODE_DIAGNOSTIC ? 100000u : 250000u;
    advance=sequence-r->command_sequence;
    if ((unsigned)mode>ATO_MODE_DIAGNOSTIC || !r->config_valid
        || epoch!=r->config_epoch || !lease_us || lease_us>max_lease
        || (r->command_seen && (!advance || advance>=0x80000000u))
        || !add_time(now_us,lease_us,&deadline)) {
        ato_runtime_trip(r,ATO_FAULT_LEASE,1,now_us);
        return false;
    }
    if (mode!=r->mode) {
        if (r->state!=ATO_STATE_IDLE) {
            ato_runtime_trip(r,ATO_FAULT_LEASE,2,now_us);
            return false;
        }
        ato_runtime_trip(r,ATO_FAULT_CONFIG,3,now_us);
    }
    r->mode=(uint8_t)mode;
    r->command_sequence=sequence;
    r->command_seen=1;
    r->lease_deadline_us=deadline;
    if (mode==ATO_MODE_OBSERVE) outputs_off(r);
    return true;
}
bool ato_runtime_recovery_begin(ato_runtime *r, uint64_t now_us) {
    const uint16_t pre_monitor=(uint16_t)(ATO_REQUIRED_HEALTH&~ATO_HEALTH_MONITORS);
    if (!clock_ok(r,now_us)) return false;
    if (r->output.armed || !r->config_valid || !r->sample_seen
        || (r->health&pre_monitor)!=pre_monitor || !quiet(r)
        || r->state!=ATO_STATE_IDLE || !lease_fresh(r,now_us)
        || (r->mode==ATO_MODE_PRESSURE && !pressure_fresh(r,now_us)))
        return false;
    /* This does not clear software fault, ARM, driver timeout, route or the
     * charge-integrator history. One explicit request produces one action. */
    r->pending_actions=ATO_ACTION_MON_REARM;
    return true;
}
bool ato_runtime_rearm(ato_runtime *r, uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!r->config_valid || !r->sample_seen || !health_ok(r) || !quiet(r)
        || r->state!=ATO_STATE_IDLE || !lease_fresh(r,now_us)
        || (r->mode==ATO_MODE_PRESSURE && !pressure_fresh(r,now_us)))
        return false;
    r->sticky_fault=ATO_FAULT_NONE;
    r->route_valid=0;
    r->route_pending=0;
    r->output.armed=1;
    r->output.diagnostic_capture=(uint8_t)(r->mode==ATO_MODE_DIAGNOSTIC);
    r->pending_actions=ATO_ACTION_FAULT_RESET|ATO_ACTION_SUP_REARM;
    changed(r);
    return true;
}
bool ato_runtime_route_prepare(ato_runtime *r, uint8_t contact0,
                               uint8_t contact1, uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!admitted(r,now_us) || !quiet(r) || r->state!=ATO_STATE_IDLE
        || (r->pending_actions&(ATO_ACTION_MON_REARM|ATO_ACTION_FAULT_RESET
                                |ATO_ACTION_SUP_REARM))
        || r->output.want_mask || contact0>15 || contact1>15) {
        ato_runtime_trip(r,ATO_FAULT_ROUTE,1,now_us);
        return false;
    }
    r->route_valid=0;
    r->route_pending=1;
    r->route_contact[0]=contact0;
    r->route_contact[1]=contact1;
    r->output.contact[0]=contact0;
    r->output.contact[1]=contact1;
    r->pending_actions|=ATO_ACTION_ROUTE_COMMIT;
    changed(r);
    return true;
}
bool ato_runtime_route_readback(ato_runtime *r, uint8_t active0,
                                uint8_t active1, uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!admitted(r,now_us) || r->route_pending!=2u || !quiet(r)
        || active0!=r->route_contact[0] || active1!=r->route_contact[1]) {
        ato_runtime_trip(r,ATO_FAULT_ROUTE,2,now_us);
        return false;
    }
    r->route_pending=0;
    r->route_valid=1;
    r->pending_actions|=ATO_ACTION_ROUTE_ACK|ATO_ACTION_ROUTE_REARM;
    changed(r);
    return true;
}
bool ato_runtime_event(ato_runtime *r, const ato_event_plan *plan,
                       uint64_t now_us) {
    unsigned i;
    if (!clock_ok(r,now_us)) return false;
    if (!plan || !admitted(r,now_us) || !quiet(r)
        || r->state!=ATO_STATE_IDLE || !r->route_valid
        || (r->pending_actions&(ATO_ACTION_ROUTE_COMMIT|ATO_ACTION_ROUTE_ACK
                                |ATO_ACTION_ROUTE_REARM))
        || (r->mode!=ATO_MODE_MOTOR && r->mode!=ATO_MODE_PRESSURE)
        || plan->epoch!=r->config_epoch || !plan->event_id
        || (r->event_seen && (uint32_t)(plan->event_id-r->plan.event_id)>=0x80000000u)
        || (r->event_seen && plan->event_id==r->plan.event_id)
        || !plan->source_mask || plan->source_mask>3u
        || !plan->phase_us || plan->phase_us>ATO_PHASE_MAX_US
        || plan->gap_us<ATO_GAP_MIN_US
        || (r->event_seen && now_us-r->last_event_us<ATO_EVENT_MIN_US)
        || (plan->source_mask==3 && plan->contact[0]==plan->contact[1])) {
        ato_runtime_trip(r,ATO_FAULT_PHASE,1,now_us);
        return false;
    }
    for (i=0;i<2;++i) {
        if (plan->contact[i]!=r->route_contact[i]
            || plan->current_ua[i]>3000u
            || ((plan->source_mask&(1u<<i)) && !plan->current_ua[i])) {
            ato_runtime_trip(r,ATO_FAULT_PHASE,2,now_us);
            return false;
        }
    }
    r->plan=*plan;
    r->event_seen=1;
    r->last_event_us=now_us;
    if (plan->off_trial) return true;
    r->state=ATO_STATE_PREPARE_FIRST;
    r->output.want_mask=plan->source_mask;
    r->output.plus_mask=plan->source_mask;
    r->output.current_ua[0]=plan->current_ua[0];
    r->output.current_ua[1]=plan->current_ua[1];
    r->phase_ready=0;
    r->pending_actions|=ATO_ACTION_PHASE_REARM;
    changed(r);
    return true;
}
bool ato_runtime_phase_ready(ato_runtime *r, uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!admitted(r,now_us) || !quiet(r)
        || (r->pending_actions&ATO_ACTION_PHASE_REARM)
        || (r->state!=ATO_STATE_PREPARE_FIRST
            && r->state!=ATO_STATE_PREPARE_SECOND)) {
        ato_runtime_trip(r,ATO_FAULT_PHASE,3,now_us);
        return false;
    }
    r->phase_ready=1;
    return true;
}
bool ato_runtime_phase_start(ato_runtime *r, uint64_t now_us) {
    uint64_t deadline;
    if (!clock_ok(r,now_us)) return false;
    if (!admitted(r,now_us) || !quiet(r) || !r->phase_ready
        || !add_time(now_us,r->plan.phase_us,&deadline)
        || (r->state!=ATO_STATE_PREPARE_FIRST
            && r->state!=ATO_STATE_PREPARE_SECOND)) {
        ato_runtime_trip(r,ATO_FAULT_PHASE,4,now_us);
        return false;
    }
    r->state=(uint8_t)(r->state==ATO_STATE_PREPARE_FIRST ? ATO_STATE_FIRST:
                                                                    ATO_STATE_SECOND);
    r->deadline_us=deadline;
    r->phase_ready=0;
    r->output.request_mask=r->plan.source_mask;
    changed(r);
    return true;
}
void ato_runtime_phase_end(ato_runtime *r, uint64_t now_us) {
    if (!clock_ok(r,now_us)) return;
    if ((r->state!=ATO_STATE_FIRST && r->state!=ATO_STATE_SECOND)
        || now_us!=r->deadline_us) {
        ato_runtime_trip(r,ATO_FAULT_PHASE,5,now_us);
        return;
    }
    r->output.request_mask=0;
    if (r->state==ATO_STATE_FIRST) {
        r->state=ATO_STATE_GAP;
        if (!add_time(now_us,r->plan.gap_us,&r->deadline_us)) {
            ato_runtime_trip(r,ATO_FAULT_CLOCK,2,now_us);
            return;
        }
    } else {
        r->state=ATO_STATE_RECOVERY;
    }
    changed(r);
}
void ato_runtime_tick(ato_runtime *r, uint64_t now_us) {
    if (!clock_ok(r,now_us)) return;
    if (r->output.armed && !lease_fresh(r,now_us)) {
        ato_runtime_trip(r,ATO_FAULT_LEASE,3,now_us);
        return;
    }
    if (r->mode==ATO_MODE_PRESSURE && r->pressure_valid
        && !pressure_fresh(r,now_us)) {
        r->pressure_valid=0;
        ato_runtime_trip(r,ATO_FAULT_STALE,1,now_us);
        return;
    }
    if (!r->output.armed) return;
    if (!admitted(r,now_us)) {
        ato_runtime_trip(r,ATO_FAULT_HEALTH,0,now_us);
        return;
    }
    if ((r->state==ATO_STATE_FIRST || r->state==ATO_STATE_SECOND)
        && now_us>=r->deadline_us) {
        /* A late ISR/poll is retained as interruption, never a synthetic
         * backdated normal phase end. Hardware timer has separate authority. */
        if (now_us>r->deadline_us)
            ato_runtime_trip(r,ATO_FAULT_PHASE,6,now_us);
        else ato_runtime_phase_end(r,now_us);
    }
    if (r->state==ATO_STATE_GAP && now_us>=r->deadline_us && quiet(r)) {
        r->state=ATO_STATE_PREPARE_SECOND;
        r->output.plus_mask=0;
        r->pending_actions|=ATO_ACTION_PHASE_REARM;
        changed(r);
    }
    if (r->state==ATO_STATE_RECOVERY && quiet(r)) {
        r->state=ATO_STATE_IDLE;
        r->output.want_mask=0;
        r->output.current_ua[0]=0;
        r->output.current_ua[1]=0;
        changed(r);
    }
}
bool ato_runtime_raw_identity(ato_runtime *r, uint32_t epoch,
                              uint32_t capture_id, uint8_t expected_channel,
                              uint8_t claimed_channel, uint64_t aperture_us,
                              bool transaction_known, bool in_range,
                              uint64_t now_us) {
    if (!clock_ok(r,now_us)) return false;
    if (!r->config_valid || epoch!=r->config_epoch || !transaction_known
        || expected_channel>7u || claimed_channel!=expected_channel
        || !in_range || aperture_us>now_us
        || (r->sample_seen && (capture_id!=r->last_capture_id+1u
                               || aperture_us<=r->last_raw_aperture_us))) {
        r->sample_seen=0;
        r->config_valid=0;
        ato_runtime_trip(r,ATO_FAULT_SAMPLE,1,now_us);
        return false;
    }
    r->last_capture_id=capture_id;
    r->last_raw_aperture_us=aperture_us;
    r->sample_seen=1;
    return true;
}
bool ato_runtime_queue_push(ato_runtime *r, bool raw, uint32_t bytes,
                            uint64_t now_us) {
    uint32_t *used,capacity;
    if (!clock_ok(r,now_us)) return false;
    used=raw ? &r->raw_queue_used : &r->normal_queue_used;
    capacity=raw ? ATO_RAW_QUEUE_CAPACITY : ATO_NORMAL_QUEUE_CAPACITY;
    if ((raw && (!r->output.diagnostic_capture || !lease_fresh(r,now_us)))
        || *used>capacity || bytes>capacity-*used) {
        ato_runtime_trip(r,ATO_FAULT_OVERRUN,raw?1:2,now_us);
        return false;
    }
    *used+=bytes;
    return true;
}
void ato_runtime_queue_drain(ato_runtime *r, bool raw, uint32_t bytes) {
    uint32_t *used;
    if (!r) return;
    used=raw ? &r->raw_queue_used : &r->normal_queue_used;
    *used=bytes>=*used ? 0u : *used-bytes;
}
uint16_t ato_runtime_take_actions(ato_runtime *r) {
    uint16_t actions;
    if (!r) return 0;
    actions=r->pending_actions;
    r->pending_actions=0;
    if ((actions&ATO_ACTION_ROUTE_COMMIT) && r->route_pending==1u)
        r->route_pending=2;
    return actions;
}
bool ato_runtime_extend_ticks(uint32_t previous, uint32_t current,
                               uint64_t accumulated, uint64_t *extended) {
    uint32_t delta=current-previous;
    if (!extended || delta>=0x80000000u || delta>UINT64_MAX-accumulated)
        return false;
    *extended=accumulated+delta;
    return true;
}
