NAME_DIR   := visualizer
VENV       := $(NAME_DIR)/.venv
PYTHON     := $(VENV)/bin/python3
STAMP      := $(VENV)/.synced
LOG        := /tmp/netpractice_visualizer.log

all: run interface

$(STAMP): $(wildcard $(NAME_DIR)/pyproject.toml $(NAME_DIR)/uv.lock)
	@cd $(NAME_DIR) && uv sync --quiet
	@touch $@

venv: $(STAMP)

visualizer: venv
	@$(PYTHON) -m $(NAME_DIR)

run: venv
	@setsid nohup $(PYTHON) -m $(NAME_DIR) > $(LOG) 2>&1 &

interface:
	@cd interface && setsid nohup ./run.sh > /dev/null 2>&1 &

clean:
	@rm -rf $(VENV) $(NAME_DIR)/.mypy_cache $(NAME_DIR)/*.egg-info
	@find . -name __pycache__ -type d -prune -exec rm -rf {} +

re: clean all

.PHONY: all venv visualizer run interface clean re