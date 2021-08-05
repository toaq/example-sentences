
.PHONY: filter

run:	stats.py
	@python3 stats.py

filter:
	@python3 filter.py
