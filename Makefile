SHELL      := /bin/bash

NAME_DIR   := visualizer
VENV       := $(NAME_DIR)/.venv
PYTHON     := $(VENV)/bin/python3
STAMP      := $(VENV)/.synced
LOG        := /tmp/netpractice_visualizer.log

all: venv
	@echo "Running... (Ctrl+C to stop)"
	@trap 'trap "" INT TERM; kill 0' INT TERM; \
	$(PYTHON) -m $(NAME_DIR) > $(LOG) 2>&1 & \
	(cd interface && exec ./run.sh > /dev/null 2>&1) & \
	wait -n; \
	trap "" INT TERM; kill 0

$(STAMP): $(wildcard $(NAME_DIR)/pyproject.toml $(NAME_DIR)/uv.lock)
	@cd $(NAME_DIR) && uv sync --quiet
	@touch $@

venv: $(STAMP)

visualizer: venv
	@$(PYTHON) -m $(NAME_DIR)

clean:
	@rm -rf $(VENV) $(NAME_DIR)/.mypy_cache $(NAME_DIR)/*.egg-info
	@find . -name __pycache__ -type d -prune -exec rm -rf {} +

re: clean all

.PHONY: all venv visualizer clean re