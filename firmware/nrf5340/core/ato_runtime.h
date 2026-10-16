#ifndef ATO_RUNTIME_H
#define ATO_RUNTIME_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* Shared production policy core. Time is monotonic local microseconds. The
 * target owns GPIO/SPIM/DPPI edges; this core never claims measured timing. */
#define ATO_SBP_PACKET_BYTES 56u
#define ATO_FAULT_LOG_CAPACITY 16u
#define ATO_PHASE_MAX_US 200u
#define ATO_GAP_MIN_US 200u
#define ATO_EVENT_MIN_US 2778u
#define ATO_RAW_QUEUE_CAPACITY 16384u
#define ATO_NORMAL_QUEUE_CAPACITY 8192u
#define ATO_REQUIRED_HEALTH 0x007fu
#define ATO_HEALTH_RESET 0x0001u
#define ATO_HEALTH_RAILS 0x0002u
#define ATO_HEALTH_WATCHDOG 0x0004u
#define ATO_HEALTH_AFE_BLANK 0x0008u
#define ATO_HEALTH_MONITORS 0x0010u
#define ATO_HEALTH_POWER 0x0020u
#define ATO_HEALTH_RAW_CONFIG 0x0040u
#define ATO_ACTION_ROUTE_COMMIT 0x0001u
#define ATO_ACTION_ROUTE_ACK 0x0002u
#define ATO_ACTION_ROUTE_REARM 0x0004u
#define ATO_ACTION_PHASE_REARM 0x0008u
#define ATO_ACTION_FAULT_RESET 0x0010u
#define ATO_ACTION_SUP_REARM 0x0020u
#define ATO_ACTION_MON_REARM 0x0040u

typedef enum {
    ATO_MODE_OBSERVE=0, ATO_MODE_MOTOR=1, ATO_MODE_PRESSURE=2,
    ATO_MODE_DIAGNOSTIC=3
} ato_mode;
typedef enum {
    ATO_STATE_IDLE=0, ATO_STATE_PREPARE_FIRST=1, ATO_STATE_FIRST=2,
    ATO_STATE_GAP=3, ATO_STATE_PREPARE_SECOND=4, ATO_STATE_SECOND=5,
    ATO_STATE_RECOVERY=6
} ato_runtime_state;
typedef enum {
    ATO_FAULT_NONE=0, ATO_FAULT_BOOT=1, ATO_FAULT_CONFIG=2,
    ATO_FAULT_HEALTH=3, ATO_FAULT_PACKET=4, ATO_FAULT_STALE=5,
    ATO_FAULT_LEASE=6, ATO_FAULT_ROUTE=7, ATO_FAULT_PHASE=8,
    ATO_FAULT_SAMPLE=9, ATO_FAULT_OVERRUN=10, ATO_FAULT_HARD_TRIP=11,
    ATO_FAULT_CLOCK=12
} ato_runtime_fault;
typedef struct {
    uint64_t at_us;
    uint32_t event_id;
    uint16_t reason;
    uint16_t detail;
} ato_fault_record;
typedef struct {
    uint32_t epoch;
    uint32_t event_id;
    uint16_t current_ua[2];
    uint16_t phase_us;
    uint16_t gap_us;
    uint8_t contact[2];
    uint8_t source_mask;
    uint8_t off_trial;
} ato_event_plan;
typedef struct {
    uint32_t generation;
    uint16_t current_ua[2];
    uint8_t contact[2];
    uint8_t request_mask;
    uint8_t plus_mask;
    uint8_t want_mask;
    uint8_t armed;
    uint8_t diagnostic_capture;
    uint8_t reserved;
} ato_runtime_output;
typedef struct {
    uint64_t now_us;
    uint64_t deadline_us;
    uint64_t lease_deadline_us;
    uint64_t last_event_us;
    uint64_t pressure_oldest_us;
    uint64_t pressure_newest_peer_us;
    uint64_t last_raw_aperture_us;
    int64_t clock_offset_lo_us;
    int64_t clock_offset_hi_us;
    uint32_t config_epoch;
    uint32_t session_epoch;
    uint32_t calibration_id;
    uint32_t pressure_sequence;
    uint32_t command_sequence;
    uint32_t last_capture_id;
    uint32_t raw_queue_used;
    uint32_t normal_queue_used;
    uint32_t fault_total;
    uint16_t health;
    uint16_t pending_actions;
    uint16_t sticky_fault;
    uint8_t quiet_mask;
    uint8_t timer_active_mask;
    uint8_t run_mask;
    uint8_t route_valid;
    uint8_t route_pending;
    uint8_t route_contact[2];
    uint8_t pressure_valid;
    uint8_t pressure_seen;
    uint8_t command_seen;
    uint8_t session_valid;
    uint8_t config_valid;
    uint8_t sample_seen;
    uint8_t event_seen;
    uint8_t phase_ready;
    uint8_t fault_head;
    uint8_t fault_count;
    uint8_t mode;
    uint8_t state;
    ato_event_plan plan;
    ato_runtime_output output;
    ato_fault_record faults[ATO_FAULT_LOG_CAPACITY];
} ato_runtime;

void ato_runtime_init(ato_runtime *r, uint64_t now_us);
bool ato_runtime_configure(ato_runtime *r, uint32_t epoch, bool readback_ok,
                           uint64_t now_us);
void ato_runtime_health(ato_runtime *r, uint16_t health, uint8_t quiet_mask,
                        uint8_t timer_active_mask, uint8_t run_mask,
                        uint64_t now_us);
bool ato_runtime_session(ato_runtime *r, uint32_t epoch, uint32_t calibration_id,
                         int64_t offset_lo_us, int64_t offset_hi_us,
                         uint64_t now_us);
bool ato_runtime_sbp(ato_runtime *r, const uint8_t *packet, size_t length,
                     uint64_t now_us);
bool ato_runtime_command(ato_runtime *r, ato_mode mode, uint32_t epoch,
                         uint32_t sequence, uint32_t lease_us,
                         uint64_t now_us);
/* Explicit inhibited recovery first qualifies pre-MON health and requests only
 * monitor-latch rearm. The backend waits observed permits before final rearm. */
bool ato_runtime_recovery_begin(ato_runtime *r, uint64_t now_us);
bool ato_runtime_rearm(ato_runtime *r, uint64_t now_us);
bool ato_runtime_route_prepare(ato_runtime *r, uint8_t contact0,
                               uint8_t contact1, uint64_t now_us);
bool ato_runtime_route_readback(ato_runtime *r, uint8_t active0,
                                uint8_t active1, uint64_t now_us);
bool ato_runtime_event(ato_runtime *r, const ato_event_plan *plan,
                       uint64_t now_us);
bool ato_runtime_phase_ready(ato_runtime *r, uint64_t now_us);
bool ato_runtime_phase_start(ato_runtime *r, uint64_t now_us);
void ato_runtime_phase_end(ato_runtime *r, uint64_t now_us);
void ato_runtime_tick(ato_runtime *r, uint64_t now_us);
void ato_runtime_trip(ato_runtime *r, ato_runtime_fault reason, uint16_t detail,
                      uint64_t now_us);
bool ato_runtime_raw_identity(ato_runtime *r, uint32_t epoch,
                              uint32_t capture_id, uint8_t expected_channel,
                              uint8_t claimed_channel, uint64_t aperture_us,
                              bool transaction_known, bool in_range,
                              uint64_t now_us);
bool ato_runtime_queue_push(ato_runtime *r, bool raw, uint32_t bytes,
                            uint64_t now_us);
void ato_runtime_queue_drain(ato_runtime *r, bool raw, uint32_t bytes);
uint16_t ato_runtime_take_actions(ato_runtime *r);
uint32_t ato_runtime_crc32(const uint8_t *bytes, size_t length);
/* A 32-bit tick delta >= half range is ambiguous and rejected. Calls must be
 * closer than 2^31 input ticks; conversion to microseconds belongs to target. */
bool ato_runtime_extend_ticks(uint32_t previous, uint32_t current,
                               uint64_t accumulated, uint64_t *extended);
#endif
