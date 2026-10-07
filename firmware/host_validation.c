#include "ato_pulse.h"
#ifdef NDEBUG
#undef NDEBUG
#endif
#include <assert.h>
#include <inttypes.h>
#include <stdio.h>

static void finish(ato_controller *c) {
    unsigned guard = 0;
    while (c->state != ATO_IDLE) {
        assert(++guard <= 4);
        ato_timer_event(c);
    }
}

int main(void) {
    ato_controller c;
    ato_config cfg = ato_default_config();
    unsigned assertions = 0;
    assert(ato_init(&c,cfg)); ++assertions;
    assert(!ato_start_pulse(&c,0)); ++assertions;
    ato_sensor_update(&c,0,true);
    assert(ato_rearm(&c,0)); ++assertions;
    assert(ato_start_pulse(&c,0)); ++assertions;
    int64_t charge = 0;
    uint32_t elapsed = 0;
    puts("start_us,current_ua,duration_us,state");
    while (c.state != ATO_IDLE) {
        printf("%" PRIu32 ",%d,%" PRIu32 ",%d\n",elapsed,c.output.current_ua,c.output.duration_us,c.state);
        charge += (int64_t)c.output.current_ua*c.output.duration_us;
        elapsed += c.output.duration_us;
        ato_timer_event(&c);
    }
    assert(charge == 0); ++assertions;
    assert(elapsed == cfg.period_us); ++assertions;
    assert(c.output.current_ua == 0); ++assertions;
    assert(!ato_start_pulse(&c,1)); ++assertions;
    ato_sensor_update(&c,20000,true);
    assert(ato_start_pulse(&c,20000)); ++assertions;
    ato_sensor_update(&c,20100,false);
    assert(c.fault == ATO_SENSOR_INVALID); ++assertions;
    charge = (int64_t)c.output.current_ua*c.output.duration_us;
    ato_timer_event(&c);
    charge += (int64_t)c.output.current_ua*c.output.duration_us;
    ato_timer_event(&c);
    assert(c.output.current_ua == -100); ++assertions;
    charge += (int64_t)c.output.current_ua*c.output.duration_us;
    finish(&c);
    assert(charge == 0); ++assertions;
    assert(!ato_start_pulse(&c,40000)); ++assertions;
    ato_sensor_update(&c,40000,true);
    assert(ato_rearm(&c,40000)); ++assertions;
    assert(!ato_start_pulse(&c,140001)); ++assertions;
    assert(c.fault == ATO_SENSOR_STALE); ++assertions;
    cfg.current_ua = 251;
    assert(!ato_init(&c,cfg)); ++assertions;
    assert(!ato_start_pulse(&c,0)); ++assertions;
    cfg = ato_default_config(); cfg.period_us = 10000;
    assert(!ato_init(&c,cfg)); ++assertions;
    cfg = ato_default_config(); cfg.phase_us = 0;
    assert(!ato_init(&c,cfg)); ++assertions;
    cfg = ato_default_config();
    assert(ato_init(&c,cfg)); ++assertions;
    ato_sensor_update(&c,UINT32_MAX-500,true);
    assert(ato_start_pulse(&c,300)); ++assertions;
    assert(!ato_start_pulse(&c,301)); ++assertions;
    finish(&c);
    fprintf(stderr,"C host validation: %u assertions passed; pulse charge = 0 nC\n",assertions);
    return 0;
}
