# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

import importlib
from profed.core.config import config

_instance = None

def init_message_bus():
    global _instance
    cfg = config().get("message_bus", {})
    typ = cfg.get("type", "postgresql")

    mod = importlib.import_module(f"profed.core.mesage_bus.{typ}")
    init = getattr(mod, "init")
    _instance = init(cfg)

def message_bus():
    return _instance
