PYTHON = visualizer/.venv/bin/python3

venv:
	cd visualizer; uv sync;

visualizer: venv
	$(PYTHON) -m visualizer

clean:
	rm -rf visualizer/.venv
	rm -rf visualizer/__pycache__
	rm -rf visualizer/.mypy_cache
	rm -rf visualizer/netpractice_visualizer.egg-info


.PHONY: visualizer venv clean