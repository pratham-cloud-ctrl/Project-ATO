#ifndef ATO_BACKEND_H
#define ATO_BACKEND_H
#include "ato_runtime.h"
#include <stdbool.h>
#include <stdint.h>

typedef struct {
    uint64_t aperture_lo_us, aperture_hi_us;
    uint32_t epoch, capture_id;
    uint16_t code;
    uint8_t channel, valid;
} ato_raw_record;
typedef struct {
    uint64_t frame_lo_us;
    uint32_t aperture_offset_lo_us[16], aperture_offset_hi_us[16];
    int16_t samples[16];
    uint32_t epoch, sequence;
    uint16_t valid_mask, supply_code;
} ato_rhd_record;
typedef struct {
    uint64_t aperture_lo_us, aperture_hi_us;
    uint32_t epoch, event_id, reset_epoch;
    uint16_t code[2];
    uint8_t phase, source_mask, valid, reserved;
} ato_endpoint_record;
typedef struct {
    uint32_t raw_received, rhd_frames, endpoint_pairs, uart_rejects;
    uint32_t missed_raw_slots, missed_rhd_frames, telemetry_dropped;
    uint32_t latest_sideband, configuration_epoch, integrator_epoch;
    uint16_t envelope[16];
    uint8_t commissioned, observing;
} ato_backend_status;

bool ato_backend_init(ato_runtime *runtime);
uint64_t ato_backend_now_us(void);
void ato_backend_service(ato_runtime *runtime);
void ato_backend_stop(void);
const ato_backend_status *ato_backend_status_get(void);
#endif
