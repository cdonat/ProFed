# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.core.config import config
from profed.core.component_manager import run
from profed.core.message_bus import init_message_bus


if __name__ == "__main__":
    run(config(), [init_message_bus])
