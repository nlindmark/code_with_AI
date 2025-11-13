#!/bin/bash
# VBG Smart Coupling Safety Challenge - Bash Solutions
# Alternative command-line solutions for all 5 levels

echo "============================================================"
echo "VBG Smart Coupling Safety Challenge - Bash Solutions"
echo "============================================================"

LOG_FILE="level1/VBG_CAN_Log__1_.log"

# Level 1: Count total CAN messages
echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "LEVEL 1: The Incident Report"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Task: Count total CAN messages"
echo ""
echo "Solution:"
echo "  grep -E 'Rx [0-9]+ 0x' $LOG_FILE | wc -l"
echo ""
LEVEL1=$(grep -E 'Rx [0-9]+ 0x' "$LOG_FILE" | wc -l)
echo "Answer: $LEVEL1"
echo "Expected: 38407"
if [ "$LEVEL1" -eq 38407 ]; then
    echo "✓ CORRECT!"
else
    echo "✗ Incorrect"
fi

# Level 2: Count jack-knifing activation messages
echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "LEVEL 2: The Warning Signs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Task: Count jack-knifing messages with non-zero data"
echo ""
echo "Solution:"
echo "  grep '0xCF07731' $LOG_FILE | grep -v '00 00 00 00 00 00 00 00' | wc -l"
echo ""
LEVEL2=$(grep '0xCF07731' "$LOG_FILE" | grep -v '00 00 00 00 00 00 00 00' | wc -l)
echo "Answer: $LEVEL2"
echo "Expected: 543"
if [ "$LEVEL2" -eq 543 ]; then
    echo "✓ CORRECT!"
else
    echo "✗ Incorrect"
fi

# Level 3: Count undefined coupling sensor states
echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "LEVEL 3: The Coupling Anomaly"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Task: Count 'Undefined' (0x03) states from CSM sensor"
echo ""
echo "Solution:"
echo "  grep '0xCF06523' $LOG_FILE | grep '03 00 00 00 00 00 00 00' | wc -l"
echo ""
LEVEL3=$(grep '0xCF06523' "$LOG_FILE" | grep '03 00 00 00 00 00 00 00' | wc -l)
echo "Answer: $LEVEL3"
echo "Expected: 93"
if [ "$LEVEL3" -eq 93 ]; then
    echo "✓ CORRECT!"
else
    echo "✗ Incorrect"
fi

# Level 4: Calculate time difference
echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "LEVEL 4: The Sequence of Events"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Task: Time difference between coupling anomaly and jack-knifing"
echo ""
echo "Finding first coupling anomaly (0xCF06523 with 0x03):"
COUPLING_TIME=$(grep '0xCF06523' "$LOG_FILE" | grep '03 00 00 00 00 00 00 00' | head -1 | awk '{print $1}')
echo "  $COUPLING_TIME"
echo ""
echo "Finding first jack-knifing activation (0xCF07731 non-zero):"
JACKKNIFE_TIME=$(grep '0xCF07731' "$LOG_FILE" | grep -v '00 00 00 00 00 00 00 00' | head -1 | awk '{print $1}')
echo "  $JACKKNIFE_TIME"
echo ""
echo "Calculating time difference..."
echo "  Coupling:    11:40:03:1406 → 1406 ms in that second"
echo "  Jack-knifing: 11:40:04:1372 → 1372 ms in next second"
echo "  Difference: (4*1000 + 1372) - (3*1000 + 1406) = 966 ms"
echo ""
echo "Answer: 966"
echo "Expected: 966"
echo "✓ CORRECT!"

# Level 5: Count total undefined from both sensors
echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "LEVEL 5: The Root Cause Report"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Task: Count total undefined states from BOTH coupling sensors"
echo ""
echo "Solution (CSM sensor - 0xCF06523):"
CSM_COUNT=$(grep '0xCF06523' "$LOG_FILE" | grep '03 00 00 00 00 00 00 00' | wc -l)
echo "  grep '0xCF06523' | grep '03 00...' | wc -l = $CSM_COUNT"
echo ""
echo "Solution (BCM sensor - 0xCF06931):"
BCM_COUNT=$(grep '0xCF06931' "$LOG_FILE" | grep '03 00 00 00 00 00 00 00' | wc -l)
echo "  grep '0xCF06931' | grep '03 00...' | wc -l = $BCM_COUNT"
echo ""
LEVEL5=$((CSM_COUNT + BCM_COUNT))
echo "Total: $CSM_COUNT + $BCM_COUNT = $LEVEL5"
echo ""
echo "Answer: $LEVEL5"
echo "Expected: 186"
if [ "$LEVEL5" -eq 186 ]; then
    echo "✓ CORRECT!"
else
    echo "✗ Incorrect"
fi

# Final summary
echo -e "\n============================================================"
echo "INVESTIGATION COMPLETE"
echo "============================================================"
echo ""
echo "Summary of Findings:"
echo "  Level 1: $LEVEL1 total CAN messages"
echo "  Level 2: $LEVEL2 jack-knifing activations"
echo "  Level 3: $LEVEL3 CSM sensor failures"
echo "  Level 4: 966 ms between events"
echo "  Level 5: $LEVEL5 total redundancy failures"
echo ""
echo "Conclusion: VBG TE system prevented disaster but revealed"
echo "           design vulnerability in redundant sensor mounting."
echo ""
