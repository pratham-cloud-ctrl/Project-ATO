#include "ato_pulse.h"
#include <string.h>

ato_config ato_default_config(void) {
    const ato_config c = {100, 200, 50, 20000, 100000};
    return c;
}

static bool valid_config(ato_config c) {
    return c.current_ua > 0 && c.current_ua <= 250 &&
        c.phase_us >= 50 && c.phase_us <= 250 &&
        c.gap_us >= 20 && c.gap_us <= 1000 &&
        c.period_us >= 20000 && c.period_us <= 2000000 &&
        c.sensor_timeout_us >= 1000 && c.sensor_timeout_us <= 1000000 &&
        (uint32_t)c.current_ua*c.phase_us <= 62500 &&
        c.period_us > (uint32_t)2*c.phase_us+c.gap_us;
}

bool ato_init(ato_controller *c, ato_config config) {
    memset(c, 0, sizeof(*c));
    c->config = config;
    c->state = ATO_IDLE;
    c->configured = valid_config(config);
    c->fault = c->configured ? ATO_OK : ATO_BAD_CONFIG;
    return c->configured;
}

void ato_sensor_update(ato_controller *c, uint32_t now_us, bool valid) {
    c->sensor_valid = valid;
    if (valid) c->sensor_time_us = now_us;
    else if (c->fault == ATO_OK) c->fault = ATO_SENSOR_INVALID;
}

void ato_poll(ato_controller *c, uint32_t now_us) {
    if (c->fault != ATO_OK) return;
    if (!c->sensor_valid) c->fault = ATO_SENSOR_INVALID;
    else if ((uint32_t)(now_us-c->sensor_time_us) > c->config.sensor_timeout_us)
        c->fault = ATO_SENSOR_STALE;
    /* Do not truncate an already scheduled balancing phase on a software fault.
       Independent hardware emergency inhibition is outside this abstraction. */
}

bool ato_start_pulse(ato_controller *c, uint32_t now_us) {
    ato_poll(c, now_us);
    if (!c->configured || c->fault != ATO_OK || c->state != ATO_IDLE) return false;
    if (c->has_started && (uint32_t)(now_us-c->last_start_us) < c->config.period_us) return false;
    c->last_start_us = now_us;
    c->has_started = true;
    c->state = ATO_POSITIVE;
    c->output.current_ua = (int16_t)c->config.current_ua;
    c->output.duration_us = c->config.phase_us;
    return true;
}

void ato_timer_event(ato_controller *c) {
    /* The backend must call once at each hardware-timer boundary. */
    switch (c->state) {
    case ATO_POSITIVE:
        c->state = ATO_GAP;
        c->output.current_ua = 0;
        c->output.duration_us = c->config.gap_us;
        break;
    case ATO_GAP:
        c->state = ATO_NEGATIVE;
        c->output.current_ua = -(int16_t)c->config.current_ua;
        c->output.duration_us = c->config.phase_us;
        break;
    case ATO_NEGATIVE:
        c->state = ATO_RECOVERY;
        c->output.current_ua = 0;
        c->output.duration_us = c->config.period_us-(uint32_t)2*c->config.phase_us-c->config.gap_us;
        break;
    case ATO_RECOVERY:
    default:
        c->state = ATO_IDLE;
        c->output.current_ua = 0;
        c->output.duration_us = 0;
        break;
    }
}

bool ato_rearm(ato_controller *c, uint32_t now_us) {
    if (!c->configured || !c->sensor_valid || c->state != ATO_IDLE ||
        (uint32_t)(now_us-c->sensor_time_us) > c->config.sensor_timeout_us) return false;
    c->fault = ATO_OK;
    return true;
}
