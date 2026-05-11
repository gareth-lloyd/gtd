ROOT := $(shell pwd)
LABEL := com.glloyd.gtd
UID := $(shell id -u)
PLIST_DEST := $(HOME)/Library/LaunchAgents/$(LABEL).plist
SERVICE := gui/$(UID)/$(LABEL)
HEALTH_URL := http://127.0.0.1:8765/api/health/

.PHONY: help serve install-service uninstall-service reinstall-service \
        restart-service service-status service-logs rebuild-frontend

help:
	@echo "GTD service management targets:"
	@echo "  make serve              Run gunicorn in foreground (debug)"
	@echo "  make install-service    Install + start LaunchAgent (login auto-start)"
	@echo "  make uninstall-service  Stop + remove LaunchAgent"
	@echo "  make reinstall-service  Uninstall then install (use after path changes)"
	@echo "  make restart-service    Restart the running LaunchAgent"
	@echo "  make service-status     Show launchd status for the agent"
	@echo "  make service-logs       Tail error + launchd stderr logs"
	@echo "  make rebuild-frontend   npm run build + restart service"

serve:
	@./scripts/serve.sh

install-service:
	@command -v uv >/dev/null || { echo "ERROR: uv not on PATH"; exit 1; }
	@command -v claude >/dev/null || { echo "ERROR: claude CLI not on PATH"; exit 1; }
	@test -d "$(ROOT)/data" || { echo "ERROR: $(ROOT)/data missing — refusing to install service against wrong repo"; exit 1; }
	@if launchctl print $(SERVICE) >/dev/null 2>&1; then \
		echo "Service already installed. Run 'make reinstall-service' to replace it."; \
		exit 1; \
	fi
	@echo "Building frontend..."
	@cd frontend && npm install --silent && npm run build
	@echo "Rendering plist..."
	@UV_BIN_DIR=$$(dirname $$(command -v uv)); \
	CLAUDE_BIN_DIR=$$(dirname $$(command -v claude)); \
	PATH_VALUE="$$UV_BIN_DIR:$$CLAUDE_BIN_DIR:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"; \
	sed -e "s|@ROOT@|$(ROOT)|g" \
	    -e "s|@HOME@|$(HOME)|g" \
	    -e "s|@PATH@|$$PATH_VALUE|g" \
	    scripts/gtd.plist.template > "$(PLIST_DEST)"
	@echo "Installed plist at $(PLIST_DEST)"
	@launchctl bootstrap gui/$(UID) "$(PLIST_DEST)"
	@echo "Bootstrapped $(SERVICE). Waiting for service to come up..."
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do \
		if curl -sf "$(HEALTH_URL)" >/dev/null 2>&1; then \
			break; \
		fi; \
		sleep 1; \
	done
	@echo "Health check:"
	@curl -sf "$(HEALTH_URL)" | python3 -m json.tool || { \
		echo "ERROR: service did not come up. Check logs/launchd.stderr.log"; exit 1; }
	@ACTUAL=$$(curl -sf "$(HEALTH_URL)" | python3 -c "import json,sys; print(json.load(sys.stdin)['data_root'])"); \
	EXPECTED="$(ROOT)/data"; \
	if [ "$$ACTUAL" != "$$EXPECTED" ]; then \
		echo "ERROR: data_root mismatch! expected=$$EXPECTED actual=$$ACTUAL"; exit 1; \
	fi
	@echo "Service installed and verified. http://127.0.0.1:8765/"

uninstall-service:
	@if launchctl print $(SERVICE) >/dev/null 2>&1; then \
		launchctl bootout $(SERVICE); \
		echo "Bootted out $(SERVICE)."; \
	else \
		echo "Service not loaded. Continuing."; \
	fi
	@rm -f "$(PLIST_DEST)"
	@echo "Removed $(PLIST_DEST)"

reinstall-service: uninstall-service install-service

restart-service:
	@launchctl kickstart -k $(SERVICE)
	@echo "Restarted $(SERVICE)."

service-status:
	@launchctl print $(SERVICE) 2>/dev/null | head -40 || echo "Service not loaded."
	@echo ""
	@echo "--- Health check ---"
	@curl -sf "$(HEALTH_URL)" | python3 -m json.tool 2>/dev/null || echo "Health endpoint unreachable."

service-logs:
	@tail -F logs/error.log logs/launchd.stderr.log

rebuild-frontend:
	@cd frontend && npm run build
	@$(MAKE) restart-service
