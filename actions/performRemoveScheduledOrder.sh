#!/bin/bash

# Removes a scheduled order
function performRemoveScheduledOrder() {
	scheduledOrder="$(cat ./.sgcli/scheduledOrders)"
	crontab -l | grep -v "$scheduledOrder" | crontab -
	rm ./.sgcli/scheduledOrders

	echo "Order removed"
}

performRemoveScheduledOrder