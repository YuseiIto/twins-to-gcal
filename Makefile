POETRY = poetry 
ARGS = $(foreach a,$($(subst -,_,$1)_args),$(if $(value $a),$a="$($a)"))

.PHONY: run
run:
	$(POETRY) run python3 main.py $(ARGS)

.PHONY: mypy
mypy:
	$(POETRY) run mypy .

.PHONY: check
check: mypy
