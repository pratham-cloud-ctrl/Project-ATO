#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include "ato_backend.h"

static ato_runtime runtime;

int main(void)
{
    ato_runtime_init(&runtime, 0);
    if (!ato_backend_init(&runtime)) {
        ato_backend_stop();
        ato_runtime_trip(&runtime, ATO_FAULT_CONFIG, 0x100, ato_backend_now_us());
        printk("ATO: commissioning failed, all requests inhibited\n");
    } else {
        printk("ATO: linked commissioning profile; explicit session/command/rearm required\n");
    }
    for (;;) {
        ato_backend_service(&runtime);
        /* No sleep is a timing guarantee. The lower-rate profile detects missed
         * slots, uses actual aperture brackets, and never catches up stale work. */
        k_yield();
    }
    return 0;
}
