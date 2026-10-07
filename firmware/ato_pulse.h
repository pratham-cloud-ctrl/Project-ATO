#ifndef ATO_PULSE_H
#define ATO_PULSE_H
#include <stdbool.h>
#include <stdint.h>
#if defined(_WIN32) && defined(ATO_SHARED)
#define ATO_API __declspec(dllexport)
#else
#define ATO_API
#endif

/* Digital reference, not a deployed MCU driver or medical device. */
typedef enum { ATO_IDLE, ATO_POSITIVE, ATO_GAP, ATO_NEGATIVE, ATO_RECOVERY } ato_state;
typedef enum { ATO_OK, ATO_BAD_CONFIG, ATO_SENSOR_INVALID, ATO_SENSOR_STALE } ato_fault;
typedef struct {
    uint16_t current_ua, phase_us, gap_us;
    uint32_t period_us, sensor_timeout_us;
} ato_config;
typedef struct {
    int16_t current_ua;
    uint32_t duration_us;
} ato_segment;
typedef struct {
    ato_config config;
    ato_state state;
    ato_fault fault;
    uint32_t sensor_time_us;
    bool sensor_valid;
    bool configured;
    ato_segment output;
    uint32_t last_start_us;
    bool has_started;
} ato_controller;

ATO_API ato_config ato_default_config(void);
ATO_API bool ato_init(ato_controller *controller, ato_config config);
ATO_API void ato_sensor_update(ato_controller *controller, uint32_t now_us, bool valid);
ATO_API void ato_poll(ato_controller *controller, uint32_t now_us);
ATO_API bool ato_start_pulse(ato_controller *controller, uint32_t now_us);
ATO_API void ato_timer_event(ato_controller *controller);
ATO_API bool ato_rearm(ato_controller *controller, uint32_t now_us);
#endif
